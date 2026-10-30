#!/usr/bin/env bash
set -e

TASK_NAME="rag_index_update"
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON_BIN="$PROJECT_DIR/.venv/bin/python"
SCRIPT="$PROJECT_DIR/src/update_index.py"

if [ ! -x "$PYTHON_BIN" ]; then
    echo "Не найден $PYTHON_BIN. Сначала: python -m venv .venv && pip install -r requirements.txt" >&2
    exit 1
fi

CRON_LINE="0 6 * * * cd $PROJECT_DIR && PYTHONPATH=$PROJECT_DIR/src $PYTHON_BIN $SCRIPT >> $PROJECT_DIR/index_update.log 2>&1"

( crontab -l 2>/dev/null | grep -v "$SCRIPT" || true ) | { cat; echo "$CRON_LINE"; } | crontab -

echo "Cron-задача '$TASK_NAME' установлена (ежедневно в 06:00)."
echo "Проверить: crontab -l | grep $SCRIPT"