# Telegram-бот для RAG-системы QuantumForge

## Обзор

Telegram-бот представляет собой пользовательский интерфейс для RAG-системы, позволяющий взаимодействовать с базой знаний Quantum Realms через мессенджер Telegram. Бот реализован на базе фреймворка aiogram и интегрирован с основным RAG-пайплайном.

## Архитектура

```
Пользователь Telegram → aiogram (Telegram API) → telegram_bot.py → RAGBot → LLM/Векторный поиск → Ответ
```

## Функциональные возможности

### Основные функции

1. **Текстовые запросы**: Обработка любых текстовых вопросов на русском языке
2. **Команды**: Поддержка стандартных команд Telegram-бота
3. **Медиа-сообщения**: Корректная обработка неподдерживаемых типов сообщений
4. **Асинхронная обработка**: Неблокирующая обработка запросов через `run_in_executor`
5. **Ограничение длины**: Проверка длины запроса (максимум 1000 символов)

### Команды бота

- `/start` - Начало работы с ботом, приветственное сообщение
- `/help` - Справка по доступным командам и возможностям
- Любой текстовый вопрос - Получение ответа из базы знаний

## Техническая реализация

### Ключевые компоненты

1. **Основной модуль**: `src/telegram_bot.py`
2. **Зависимости**: aiogram, asyncio, dotenv
3. **Интеграция**: Импорт `RAGBot` из `rag_bot.py`
4. **Конфигурация**: Настройки через `.env` файл

## Настройка и развертывание

### Требования

1. Python 3.11+
2. Установленные зависимости из `requirements.txt`
3. Токен Telegram-бота от @BotFather
4. Построенный векторный индекс (`faiss.index`)

### Конфигурация

Основные переменные окружения в `.env`:

```bash
TELEGRAM_BOT_TOKEN=ваш_токен_здесь
LLM_PROVIDER=auto  # или yandex, openai, ollama, stub
DEMO_MODE=true     # для демо-режима без API-ключей
```

### Процесс запуска

1. **Подготовка окружения**:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # или .venv\Scripts\activate.ps1
   pip install -r requirements.txt
   ```

2. **Настройка конфигурации**:

   ```bash
    .env # установка TELEGRAM_BOT_TOKEN и других переменных
   ```

3. **Подготовка данных**:

   ```bash
   python src/generate_knowledge_base.py
   python src/build_index.py
   ```

4. **Запуск бота**:
   ```bash
   python src/telegram_bot.py
   ```

### Вариант Docker

Используйте существующий `Dockerfile` и `docker-compose.yml`:

```bash
docker-compose up -d
```

#### Вариант 3: Виртуальное окружение с мониторингом

```bash
# Установка screen
screen -S telegram_bot python src/telegram_bot.py

# Или использование nohup
nohup python src/telegram_bot.py > bot.log 2>&1 &
```

## Мониторинг и логирование

### Логирование

Бот использует стандартный модуль logging Python. Логи выводятся в консоль с уровнем INFO. Для сохранения логов в файл:

```bash
python src/telegram_bot.py > telegram_bot.log 2>&1
```
