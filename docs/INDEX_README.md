# Векторный индекс базы знаний

## Модель эмбеддингов

| Параметр | Значение |
|---|---|
| Название | `sentence-transformers/all-MiniLM-L6-v2` |
| Репозиторий | https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2 |
| Размерность | 384 |
| Макс. длина последовательности | 256 токенов |
| Тип | bi-encoder, mean-pooled, cosine similarity |

## Векторная БД

| Параметр | Значение |
|---|---|
| БД | FAISS (CPU) |
| Тип индекса | `IndexFlatIP` (точное косинусное сходство через L2-нормализацию) |
| Метрика | cosine similarity |
| Top-K по умолчанию | 3 (расширен до 5 для последующей фильтрации) |
| Порог релевантности | 0.45 |

## База знаний

| Параметр | Значение |
|---|---|
| Папка | `knowledge_base/` |
| Всего документов | 32 (уникальная база Quantum Realms на основе Star Wars) |
| Сплиттер | `RecursiveCharacterTextSplitter` |
| Размер чанка | 500 символов |
| Перекрытие | 50 символов |
| Чанков в индексе | ~90 (зависит от длины документов) |
| Время индексации | см. `index_metadata.json` |

## Артефакты (в корне проекта)

| Файл | Описание |
|---|---|
| `../faiss.index` | Векторный индекс FAISS (бинарный) |
| `../index_metadata.pkl` | Метаданные индекса (модель, размерность, число чанков, время) |
| `../index_chunks.pkl` | Чанки с метаданными (источник, заголовок, chunk_id) |
| `../index_metadata.json` | Метаданные в человекочитаемом виде |

## Сборка

```bash
PYTHONPATH=./src python src/build_index.py
```

После запуска проверить `../index_metadata.json` — там зафиксировано фактическое время индексации.

## Пример запроса

```python
from rag_bot import RAGBot

bot = RAGBot()
results = bot.search("Кто такой Xarn Velgor?", k=3)
for r in results:
    print(r["source"], r["similarity"])
```