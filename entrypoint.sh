#!/bin/sh
set -e

cd "$(dirname "$0")"

if [ ! -f "faiss.index" ]; then
    echo "FAISS-индекс не найден, запускаю build_index.py..."
    PYTHONPATH=./src python src/build_index.py
fi

if [ -n "$TELEGRAM_BOT_TOKEN" ]; then
    exec env PYTHONPATH=./src python src/telegram_bot.py
else
    exec env PYTHONPATH=./src python src/rag_bot.py
fi