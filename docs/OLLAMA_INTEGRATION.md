# Интеграция Ollama как альтернативы YandexGPT

## Обзор

В рамках проекта реализована поддержка Ollama как локальной альтернативы облачным LLM-провайдерам (YandexGPT, OpenAI). Ollama позволяет запускать большие языковые модели локально, что обеспечивает:

1. **Конфиденциальность данных** - обработка запросов происходит локально
2. **Снижение затрат** - отсутствие платы за API-вызовы
3. **Гибкость конфигурации** - возможность выбора различных моделей
4. **Автономную работу** - функционирование без интернет-соединения

## Установка Ollama

### 1. Установка Ollama

- Скачать установщик с официального сайта: https://ollama.com/download
- Запустить установщик и следовать инструкциям

### 2. Установка моделей

```bash
# Установка модели qwen2.5-coder:32b-instruct
ollama pull qwen2.5-coder:32b-instruct

# Альтернативные модели для тестирования
ollama pull llama3.2:3b
ollama pull mistral:7b
ollama pull gemma2:2b
```

### 3. Запуск сервера Ollama

```bash
# Запуск сервера в фоновом режиме
ollama serve

# Проверка доступных моделей
ollama list
```

## Настройка проекта

### Конфигурация .env файла

Создайте файл `.env` на основе `.env.example`:

```env
# Выбор провайдера LLM
LLM_PROVIDER=ollama

# Настройки Ollama
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=qwen2.5-coder:32b-instruct

# Общие параметры LLM
LLM_TEMPERATURE=0.2
LLM_MAX_TOKENS=800
LLM_TIMEOUT=120  # Увеличенный таймаут для локальных моделей

```

### Быстрая проверка подключения

```bash
# Тестирование подключения к Ollama
python test_ollama_integration.py

# Тестирование всей цепочки RAG с Ollama
python test_llm_integration.py
```

## Использование в проекте

### Переключение между провайдерами

Проект поддерживает несколько способов выбора провайдера:

**Через файл .env**:

```env
LLM_PROVIDER=ollama
```

### Программное переключение

```python
from src.llm_clients import get_llm_client

# Использование Ollama
ollama_client = get_llm_client(provider="ollama")
response = ollama_client.generate("Привет!", system="")

# Использование YandexGPT
yandex_client = get_llm_client(provider="yandex")

# Автоматический выбор
auto_client = get_llm_client()  # или get_llm_client(provider="auto")
```

## Сравнение провайдеров

| Параметр               | YandexGPT       | Ollama            | OpenAI          |
| ---------------------- | --------------- | ----------------- | --------------- |
| **Стоимость**          | Плата за токены | Бесплатно         | Плата за токены |
| **Конфиденциальность** | Облако          | Локально          | Облако          |
| **Скорость**           | Высокая         | Зависит от железа | Высокая         |
| **Требования**         | API-ключ        | Локальный сервер  | API-ключ        |
| **Модели**             | YandexGPT       | Множество моделей | GPT-4, GPT-3.5  |

## Оптимизация производительности Ollama

### Для моделей 7B-13B параметров:

```env
LLM_MAX_TOKENS=1024
LLM_TIMEOUT=60
```

### Для моделей 32B+ параметров (qwen2.5-coder:32b):

```env
LLM_MAX_TOKENS=512  # Уменьшить для быстрых ответов
LLM_TIMEOUT=120     # Увеличить таймаут
```

### Аппаратные рекомендации:

- **CPU**: Минимум 8 ядер для моделей 7B
- **RAM**: 16GB для моделей 7B, 32GB+ для моделей 32B
- **GPU**: Рекомендуется NVIDIA с 16GB+ VRAM

## Устранение неполадок

### 1. Сервер Ollama не отвечает

```bash
# Проверка статуса сервера
curl http://localhost:11434/api/tags

# Перезапуск сервера
ollama serve
```

### 2. Модель не загружается

```bash
# Проверка установленных моделей
ollama list

# Переустановка модели
ollama rm qwen2.5-coder:32b-instruct
ollama pull qwen2.5-coder:32b-instruct
```

### 3. Таймауты при генерации

Увеличить таймаут в `.env`:

```env
LLM_TIMEOUT=180  # 3 минуты
```

### 4. Недостаточно памяти

Использовать меньшую модель:

```env
OLLAMA_MODEL=llama3.2:3b
```

## Примеры использования

### Консольный RAG-бот с Ollama

```bash
# Установка переменных окружения
$env:LLM_PROVIDER="ollama"
$env:OLLAMA_BASE_URL="http://localhost:11434/v1"

# Запуск бота
python src/rag_bot.py
```
