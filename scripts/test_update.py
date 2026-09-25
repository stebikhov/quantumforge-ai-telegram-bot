import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
from update_index import main, load_state, scan_for_changes, KNOWLEDGE_BASE_DIR

new_doc = """# Тестовый документ для обновления

Это новый документ, добавленный для тестирования автоматического обновления индекса.

## Раздел 1

Здесь содержится информация о тестовом обновлении базы знаний Quantum Realms.

## Раздел 2

Автоматическое обновление позволяет поддерживать актуальность векторного индекса.
"""

test_filename = "99_test_update.md"
test_filepath = os.path.join(KNOWLEDGE_BASE_DIR, test_filename)

with open(test_filepath, 'w', encoding='utf-8') as f:
    f.write(new_doc)

print(f"Создан тестовый документ: {test_filepath}")

print("\nЗапуск обновления индекса...\n")
main()

print("\nПроверка логов...")
log_path = PROJECT_ROOT / "update_log.jsonl"
if log_path.exists():
    with open(log_path, 'r', encoding='utf-8') as f:
        logs = f.readlines()
        if logs:
            last_log = logs[-1]
            print(f"Последняя запись лога: {last_log[:200]}...")

print("\nОчистка тестового файла...")
os.remove(test_filepath)

print("\nПовторный запуск (должно быть 'изменений не найдено')...")
main()
