import os
import json
import time
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle
from config import (
    KNOWLEDGE_BASE_DIR, INDEX_FILE, METADATA_FILE, CHUNKS_FILE,
    INDEX_METADATA_JSON, MODEL_NAME, CHUNK_SIZE, CHUNK_OVERLAP,
    get_text_splitter, load_documents, split_documents
)


def build_index(chunks):
    model = SentenceTransformer(MODEL_NAME)
    texts = [chunk.page_content for chunk in chunks]
    start = time.time()
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
    elapsed = time.time() - start
    dimension = embeddings.shape[1]
    faiss.normalize_L2(embeddings)
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)
    return index, embeddings, model, elapsed


def save_index(index, chunks, metadata):
    faiss.write_index(index, INDEX_FILE)
    with open(METADATA_FILE, "wb") as f:
        pickle.dump(metadata, f)
    with open(CHUNKS_FILE, "wb") as f:
        pickle.dump(chunks, f)
    print(f"Индекс сохранён: {INDEX_FILE}")
    print(f"Метаданные сохранены: {METADATA_FILE}")
    print(f"Чанки сохранены: {CHUNKS_FILE}")


def main():
    print("Загрузка документов...")
    documents = load_documents(KNOWLEDGE_BASE_DIR)
    print(f"Загружено документов: {len(documents)}")

    print("Разбиение на чанки...")
    chunks = split_documents(documents)
    print(f"Создано чанков: {len(chunks)}")

    print("Генерация эмбеддингов и построение индекса...")
    index, embeddings, model, elapsed = build_index(chunks)

    metadata = {
        "model_name": MODEL_NAME,
        "model_repo": "https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2",
        "dimension": int(embeddings.shape[1]),
        "num_chunks": len(chunks),
        "num_documents": len(documents),
        "chunk_size": CHUNK_SIZE,
        "chunk_overlap": CHUNK_OVERLAP,
        "embedding_time_seconds": round(elapsed, 2),
        "index_type": "FAISS IndexFlatIP (cosine similarity via L2-normalized vectors)",
    }

    save_index(index, chunks, metadata)
    with open(INDEX_METADATA_JSON, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    print(f"\nГотово! Индекс содержит {len(chunks)} чанков, размерность {embeddings.shape[1]}, время индексации {elapsed:.2f}с")


if __name__ == "__main__":
    main()
