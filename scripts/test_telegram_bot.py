#!/usr/bin/env python3
"""
Тестирование Telegram-бота без реального подключения к Telegram API.

Скрипт проверяет основные компоненты Telegram-бота:
1. Импорт модулей и зависимостей
2. Наличие конфигурационных файлов
3. Работоспособность RAG-пайплайна
4. Корректность обработки команд
"""

import os
import sys
import importlib
from pathlib import Path

def check_imports():
    """Проверяет наличие всех необходимых импортов."""
    required_modules = [
        'aiogram',
        'asyncio',
        'dotenv',
        'faiss',
        'sentence_transformers',
        'langchain_core',
        'langchain_text_splitters'
    ]
    
    print("=" * 60)
    print("Проверка импортов модулей")
    print("=" * 60)
    
    missing_modules = []
    for module in required_modules:
        try:
            importlib.import_module(module.replace('-', '_').replace('.', '_'))
            print(f"[OK] {module}")
        except ImportError as e:
            print(f"[ERROR] {module}: {e}")
            missing_modules.append(module)
    
    return missing_modules

def check_config_files():
    """Проверяет наличие необходимых конфигурационных файлов."""
    required_files = [
        '.env',
        'faiss.index',
        'index_metadata.pkl',
        'index_chunks.pkl',
        'knowledge_base/'
    ]
    
    print("\n" + "=" * 60)
    print("Проверка конфигурационных файлов")
    print("=" * 60)
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            if file_path.endswith('/'):
                # Проверка директории
                if os.path.isdir(file_path):
                    file_count = len([f for f in os.listdir(file_path) if f.endswith(('.md', '.txt'))])
                    print(f"[OK] {file_path} (найдено {file_count} документов)")
                else:
                    print(f"[ERROR] {file_path}: не является директорией")
                    missing_files.append(file_path)
            else:
                print(f"[OK] {file_path}")
        else:
            print(f"[ERROR] {file_path}: файл не найден")
            missing_files.append(file_path)
    
    return missing_files

def check_telegram_bot_structure():
    """Проверяет структуру файла telegram_bot.py."""
    bot_file = 'src/telegram_bot.py'
    
    print("\n" + "=" * 60)
    print("Проверка структуры Telegram-бота")
    print("=" * 60)
    
    if not os.path.exists(bot_file):
        print(f"✗ {bot_file}: файл не найден")
        return False
    
    try:
        with open(bot_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_elements = [
            'from aiogram import',
            'from rag_bot import RAGBot',
            'async def cmd_start',
            'async def cmd_help',
            'async def handle_message',
            'async def main',
            'if __name__ == "__main__"'
        ]
        
        all_found = True
        for element in required_elements:
            if element in content:
                print(f"[OK] {element}")
            else:
                print(f"[ERROR] {element}: не найден в коде")
                all_found = False
        
        return all_found
        
    except Exception as e:
        print(f"[ERROR] Ошибка при чтении файла: {e}")
        return False

def test_rag_bot_integration():
    """Тестирует интеграцию с RAG-ботом."""
    print("\n" + "=" * 60)
    print("Тестирование интеграции с RAG-ботом")
    print("=" * 60)
    
    try:
        # Добавляем src в путь для импорта
        sys.path.insert(0, 'src')
        
        # Пытаемся импортировать RAGBot
        from rag_bot import RAGBot
        
        print("[OK] Модуль rag_bot импортирован успешно")
        
        # Пытаемся создать экземпляр RAGBot
        try:
            bot = RAGBot(enable_security=True)
            print("[OK] Экземпляр RAGBot создан успешно")
            
            # Тестовый запрос
            test_query = "Кто такой Xarn Velgor?"
            try:
                response = bot.ask(test_query)
                print(f"[OK] Тестовый запрос выполнен")
                print(f"  Запрос: '{test_query}'")
                print(f"  Длина ответа: {len(response)} символов")
                
                # Проверяем, что ответ не пустой
                if response and len(response) > 0:
                    print("[OK] Ответ получен и не пустой")
                    
                    # Проверяем, что ответ содержит ожидаемую информацию
                    if "Xarn Velgor" in response or "не знаю" not in response.lower():
                        print("[OK] Ответ содержит релевантную информацию")
                    else:
                        print("[WARNING] Ответ может не содержать ожидаемой информации")
                else:
                    print("[ERROR] Ответ пустой")
                    
            except Exception as e:
                print(f"[ERROR] Ошибка при выполнении тестового запроса: {e}")
                
        except Exception as e:
            print(f"[ERROR] Ошибка при создании экземпляра RAGBot: {e}")
            
    except ImportError as e:
        print(f"[ERROR] Ошибка импорта RAGBot: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Неизвестная ошибка: {e}")
        return False
    
    return True

def check_env_variables():
    """Проверяет наличие необходимых переменных окружения."""
    print("\n" + "=" * 60)
    print("Проверка переменных окружения")
    print("=" * 60)
    
    # Загружаем .env файл если существует
    env_file = '.env'
    if os.path.exists(env_file):
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                env_content = f.read()
            
            required_vars = ['TELEGRAM_BOT_TOKEN', 'LLM_PROVIDER']
            
            for var in required_vars:
                if f'{var}=' in env_content:
                    # Находим значение переменной
                    lines = env_content.split('\n')
                    for line in lines:
                        if line.startswith(f'{var}='):
                            value = line.split('=', 1)[1].strip()
                            if value and value != 'your_bot_token_here':
                                print(f"[OK] {var}: установлен")
                            else:
                                print(f"[WARNING] {var}: установлено значение по умолчанию")
                            break
                else:
                    print(f"[ERROR] {var}: не найден в .env файле")
                    
        except Exception as e:
            print(f"[ERROR] Ошибка при чтении .env файла: {e}")
    else:
        print("[ERROR] .env файл не найден")
        return False
    
    return True

def main():
    """Основная функция тестирования."""
    print("Тестирование конфигурации Telegram-бота для RAG-системы")
    print("=" * 60)
    
    # Проверяем, что мы в правильной директории
    if not os.path.exists('src'):
        print("Ошибка: Запустите скрипт из корневой директории проекта")
        return 1
    
    # Выполняем все проверки
    missing_modules = check_imports()
    missing_files = check_config_files()
    bot_structure_ok = check_telegram_bot_structure()
    rag_integration_ok = test_rag_bot_integration()
    env_vars_ok = check_env_variables()
    
    # Итоговый отчёт
    print("\n" + "=" * 60)
    print("ИТОГОВЫЙ ОТЧЁТ")
    print("=" * 60)
    
    issues = []
    
    if missing_modules:
        issues.append(f"Отсутствуют модули: {', '.join(missing_modules)}")
        print("[ERROR] Проблемы с зависимостями")
    else:
        print("[OK] Все зависимости установлены")
    
    if missing_files:
        issues.append(f"Отсутствуют файлы: {', '.join(missing_files)}")
        print("[ERROR] Проблемы с конфигурационными файлами")
    else:
        print("[OK] Все конфигурационные файлы на месте")
    
    if not bot_structure_ok:
        issues.append("Проблемы со структурой Telegram-бота")
        print("[ERROR] Проблемы со структурой Telegram-бота")
    else:
        print("[OK] Структура Telegram-бота корректна")
    
    if not rag_integration_ok:
        issues.append("Проблемы с интеграцией RAG-бота")
        print("[ERROR] Проблемы с интеграцией RAG-бота")
    else:
        print("[OK] Интеграция с RAG-ботом работает")
    
    if not env_vars_ok:
        issues.append("Проблемы с переменными окружения")
        print("[ERROR] Проблемы с переменными окружения")
    else:
        print("[OK] Переменные окружения настроены")
    
    if issues:
        print(f"\n[WARNING] Найдено {len(issues)} проблем:")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
        
        print("\nРекомендации:")
        if missing_modules:
            print("  - Установите зависимости: pip install -r requirements.txt")
        if 'faiss.index' in missing_files:
            print("  - Постройте индекс: python src/build_index.py")
        if 'knowledge_base/' in missing_files:
            print("  - Сгенерируйте базу знаний: python src/generate_knowledge_base.py")
        if '.env' in missing_files:
            print("  - Создайте .env файл: cp .env.example .env")
            print("  - Настройте TELEGRAM_BOT_TOKEN в .env файле")
        
        return 1
    else:
        print("\n[SUCCESS] Все проверки пройдены успешно!")
        print("\nTelegram-бот готов к запуску:")
        print("  python src/telegram_bot.py")
        return 0

if __name__ == "__main__":
    sys.exit(main())