import os
import sys
import json
import hashlib
import pickle
import logging
from logging.handlers import RotatingFileHandler
import faiss
import numpy as np
from datetime import datetime
from sentence_transformers import SentenceTransformer
from langchain_core.documents import Document
from config import (
    KNOWLEDGE_BASE_DIR, INDEX_FILE, METADATA_FILE, CHUNKS_FILE,
    PROJECT_ROOT, MODEL_NAME, CHUNK_SIZE, CHUNK_OVERLAP, get_text_splitter,
    load_documents, split_documents
)

LOG_FILE = str(PROJECT_ROOT / "update_log.jsonl")
STATE_FILE = str(PROJECT_ROOT / "index_state.json")


def setup_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        file_handler = RotatingFileHandler(
            str(PROJECT_ROOT / 'index_update.log'),
            encoding='utf-8',
            maxBytes=5 * 1024 * 1024,
            backupCount=3
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    return logger


logger = setup_logging()


def get_file_hash(filepath):
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"files": {}}


def save_state(state):
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def log_update(log_entry):
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')


def scan_for_changes(state):
    current_files = {}
    new_files = []
    modified_files = []
    deleted_files = []

    for filename in os.listdir(KNOWLEDGE_BASE_DIR):
        if filename.endswith((".md", ".txt")):
            filepath = os.path.join(KNOWLEDGE_BASE_DIR, filename)
            file_hash = get_file_hash(filepath)
            current_files[filename] = file_hash

            if filename not in state["files"]:
                new_files.append(filename)
            elif state["files"][filename] != file_hash:
                modified_files.append(filename)

    for filename in state["files"]:
        if filename not in current_files:
            deleted_files.append(filename)

    return new_files, modified_files, deleted_files, current_files


def generate_embeddings(chunks, model):
    texts = [chunk.page_content for chunk in chunks]
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
    faiss.normalize_L2(embeddings)
    return embeddings


def update_index(new_files, modified_files, deleted_files):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "new_files": new_files,
        "modified_files": modified_files,
        "deleted_files": deleted_files,
        "new_chunks": 0,
        "total_chunks": 0,
        "errors": []
    }

    try:
        model = SentenceTransformer(MODEL_NAME)
        text_splitter = get_text_splitter()

        if deleted_files:
            logger.info(f"Удаление {len(deleted_files)} файлов из индекса...")
            if os.path.exists(CHUNKS_FILE):
                with open(CHUNKS_FILE, 'rb') as f:
                    all_chunks = pickle.load(f)
                all_chunks = [c for c in all_chunks if c.metadata.get('source') not in deleted_files]

                texts = [c.page_content for c in all_chunks]
                embeddings = model.encode(texts, convert_to_numpy=True)
                faiss.normalize_L2(embeddings)

                dimension = embeddings.shape[1]
                index = faiss.IndexFlatIP(dimension)
                index.add(embeddings)

                faiss.write_index(index, INDEX_FILE)
                with open(CHUNKS_FILE, 'wb') as f:
                    pickle.dump(all_chunks, f)

                if os.path.exists(METADATA_FILE):
                    with open(METADATA_FILE, 'rb') as f:
                        meta = pickle.load(f)
                    meta['num_chunks'] = len(all_chunks)
                    meta['dimension'] = int(dimension)
                    with open(METADATA_FILE, 'wb') as f:
                        pickle.dump(meta, f)

                log_entry["deleted_count"] = len(deleted_files)
                logger.info(f"Удалено чанков: {len(deleted_files)}")

        files_to_process = new_files + modified_files
        if files_to_process:
            logger.info(f"Обработка {len(files_to_process)} файлов...")
            documents = []
            for filename in files_to_process:
                filepath = os.path.join(KNOWLEDGE_BASE_DIR, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                documents.append(Document(
                    page_content=content,
                    metadata={"source": filename, "title": filename.replace(".md", "")}
                ))
            new_chunks = split_documents(documents)

            existing_chunk_count = 0
            if os.path.exists(CHUNKS_FILE):
                with open(CHUNKS_FILE, 'rb') as f:
                    existing_chunk_count = len(pickle.load(f))

            for i, chunk in enumerate(new_chunks):
                chunk.metadata["chunk_id"] = existing_chunk_count + i

            new_embeddings = generate_embeddings(new_chunks, model)

            if os.path.exists(INDEX_FILE) and os.path.exists(CHUNKS_FILE):
                existing_index = faiss.read_index(INDEX_FILE)
                with open(CHUNKS_FILE, 'rb') as f:
                    existing_chunks = pickle.load(f)

                all_chunks = existing_chunks + new_chunks
                all_texts = [c.page_content for c in all_chunks]
                all_embeddings = model.encode(all_texts, convert_to_numpy=True)
                faiss.normalize_L2(all_embeddings)

                dimension = all_embeddings.shape[1]
                index = faiss.IndexFlatIP(dimension)
                index.add(all_embeddings)

                faiss.write_index(index, INDEX_FILE)
                with open(CHUNKS_FILE, 'wb') as f:
                    pickle.dump(all_chunks, f)

                if os.path.exists(METADATA_FILE):
                    with open(METADATA_FILE, 'rb') as f:
                        meta = pickle.load(f)
                    meta['num_chunks'] = len(all_chunks)
                    meta['dimension'] = int(dimension)
                    with open(METADATA_FILE, 'wb') as f:
                        pickle.dump(meta, f)

                log_entry["new_chunks"] = len(new_chunks)
                log_entry["total_chunks"] = len(all_chunks)
            else:
                dimension = new_embeddings.shape[1]
                index = faiss.IndexFlatIP(dimension)
                index.add(new_embeddings)

                faiss.write_index(index, INDEX_FILE)
                with open(CHUNKS_FILE, 'wb') as f:
                    pickle.dump(new_chunks, f)

                if not os.path.exists(METADATA_FILE):
                    with open(METADATA_FILE, 'wb') as f:
                        pickle.dump({
                            "model_name": MODEL_NAME,
                            "dimension": int(dimension),
                            "num_chunks": len(new_chunks),
                            "chunk_size": CHUNK_SIZE,
                            "chunk_overlap": CHUNK_OVERLAP,
                        }, f)

                log_entry["new_chunks"] = len(new_chunks)
                log_entry["total_chunks"] = len(new_chunks)

            logger.info(f"Добавлено {len(new_chunks)} новых чанков")

        log_entry["status"] = "success"
        log_entry["index_size"] = os.path.getsize(INDEX_FILE) if os.path.exists(INDEX_FILE) else 0

    except Exception as e:
        logger.error(f"Ошибка при обновлении индекса: {e}")
        log_entry["status"] = "error"
        log_entry["errors"].append(str(e))

    log_update(log_entry)
    return log_entry


def main():
    logger.info("="*60)
    logger.info("Запуск обновления индекса базы знаний")
    logger.info("="*60)

    state = load_state()
    new_files, modified_files, deleted_files, current_files = scan_for_changes(state)

    logger.info(f"Найдено новых файлов: {len(new_files)}")
    logger.info(f"Найдено изменённых файлов: {len(modified_files)}")
    logger.info(f"Найдено удалённых файлов: {len(deleted_files)}")

    if not new_files and not modified_files and not deleted_files:
        logger.info("Изменений не найдено. Индекс актуален.")
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "status": "no_changes",
            "new_files": [],
            "modified_files": [],
            "deleted_files": [],
            "new_chunks": 0,
            "total_chunks": 0,
            "errors": []
        }
        log_update(log_entry)
        return

    log_entry = update_index(new_files, modified_files, deleted_files)

    state["files"] = current_files
    save_state(state)

    logger.info("="*60)
    logger.info(f"Обновление завершено. Статус: {log_entry.get('status', 'unknown')}")
    logger.info(f"Добавлено чанков: {log_entry.get('new_chunks', 0)}")
    logger.info(f"Всего чанков: {log_entry.get('total_chunks', 0)}")
    logger.info("="*60)


if __name__ == "__main__":
    main()
