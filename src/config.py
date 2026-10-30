from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_BASE_DIR = str(PROJECT_ROOT / "knowledge_base")

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
SEPARATORS = ["\n##", "\n###", "\n\n", "\n", " ", ""]

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
INDEX_FILE = str(PROJECT_ROOT / "faiss.index")
METADATA_FILE = str(PROJECT_ROOT / "index_metadata.pkl")
CHUNKS_FILE = str(PROJECT_ROOT / "index_chunks.pkl")
INDEX_METADATA_JSON = str(PROJECT_ROOT / "index_metadata.json")

SIMILARITY_THRESHOLD = 0.45
MAX_QUERY_LENGTH = 1000
SECURITY_ENABLED = True

# Настройки LLM по умолчанию
DEFAULT_LLM_PROVIDER = "yandex"  # yandex, openai, ollama, stub
DEFAULT_LLM_MODEL = "yandexgpt-lite"  # yandexgpt-lite, gpt-4o-mini, qwen2.5-coder:32b-instruct, etc.
DEFAULT_EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Параметры для Ollama
OLLAMA_BASE_URL = "http://localhost:11434/v1"
OLLAMA_DEFAULT_MODEL = "qwen2.5-coder:32b-instruct"

# Параметры для демонстрационного режима
DEMO_MODE = False  # Если True, использует StubLLMClient для демонстрации без API-ключей
DEMO_RESPONSES = [
    "Это демонстрационный ответ. В реальном режиме здесь был бы ответ от LLM.",
    "Демо-режим: ответ сгенерирован на основе найденных фрагментов.",
    "В рабочем режиме LLM сформировала бы развернутый ответ."
]


def get_text_splitter():
    return RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=SEPARATORS,
    )


def load_documents(directory=None):
    documents = []
    if directory is None:
        directory = KNOWLEDGE_BASE_DIR
    if not os.path.isdir(directory):
        return documents
    for filename in sorted(os.listdir(directory)):
        if not filename.endswith((".md", ".txt")):
            continue
        if filename.startswith("00_") or filename.lower().startswith("security_test"):
            continue
        filepath = os.path.join(directory, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        doc = Document(
            page_content=content,
            metadata={"source": filename, "title": filename.replace(".md", "")}
        )
        documents.append(doc)
    return documents


def split_documents(documents):
    text_splitter = get_text_splitter()
    chunks = text_splitter.split_documents(documents)
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = i
    return chunks
