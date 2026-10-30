import os
import sys
import json
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from rag_bot import RAGBot
from config import SIMILARITY_THRESHOLD, MAX_QUERY_LENGTH

GOLDEN_QUESTIONS_FILE = str(PROJECT_ROOT / "golden_questions.txt")
LOGS_FILE = str(PROJECT_ROOT / "evaluation_logs.jsonl")


def setup_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler = RotatingFileHandler(
            str(PROJECT_ROOT / 'evaluation.log'),
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


def load_golden_questions(filepath):
    questions = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split('|')
            if len(parts) >= 3:
                questions.append({
                    'question': parts[0].strip(),
                    'should_answer': parts[1].strip().lower() == 'да',
                    'category': parts[2].strip()
                })
    return questions


def extract_final_answer(response):
    """Извлекает финальный ответ из форматированного вывода бота."""
    if 'Ответ:' in response:
        idx = response.index('Ответ:')
        return response[idx + len('Ответ:'):].strip().split('\n')[0].strip()
    return response


def evaluate_response(response, should_answer, sources):
    final_answer = extract_final_answer(response).lower()

    dont_know_phrases = [
        'не знаю',
        'не могу ответить',
        'нет информации',
        'подозрительные паттерны',
        'вредоносный контент',
    ]
    says_i_dont_know = any(phrase in final_answer for phrase in dont_know_phrases)

    if should_answer:
        if says_i_dont_know:
            return False
        if not sources:
            return False
        return True
    else:
        return says_i_dont_know


def extract_sources(response):
    sources = []
    if 'источники:' in response.lower():
        idx = response.lower().index('источники:')
        sources_str = response[idx + len('источники:'):].strip()
        sources = [s.strip() for s in sources_str.split(',')]
    return sources


def run_evaluation():
    print("="*60)
    print("Автоматическая оценка качества RAG-бота")
    print("="*60)

    bot = RAGBot(enable_security=True)
    questions = load_golden_questions(GOLDEN_QUESTIONS_FILE)

    print(f"Загружено вопросов: {len(questions)}")

    logs = []
    results = {
        'total': 0,
        'correct': 0,
        'incorrect': 0,
        'by_category': {},
        'by_should_answer': {'yes': {'total': 0, 'correct': 0}, 'no': {'total': 0, 'correct': 0}}
    }

    for q in questions:
        results['total'] += 1
        category = q['category']
        if category not in results['by_category']:
            results['by_category'][category] = {'total': 0, 'correct': 0}
        results['by_category'][category]['total'] += 1

        answer_type = 'yes' if q['should_answer'] else 'no'
        results['by_should_answer'][answer_type]['total'] += 1

        print(f"\nВопрос: {q['question']}")
        print(f"Ожидаемый ответ: {'должен ответить' if q['should_answer'] else 'должен сказать не знаю'}")

        response = bot.ask(q['question'])
        sources = extract_sources(response)
        is_correct = evaluate_response(response, q['should_answer'], sources)

        expected = "должен ответить" if q['should_answer'] else "должен сказать 'не знаю'"
        final_answer = extract_final_answer(response)
        actual = "ответил" if (not ('не знаю' in final_answer.lower() or 'не могу' in final_answer.lower())) else "сказал 'не знаю'"

        print(f"Ожидаемый: {expected}, Фактический: {actual}, is_correct={is_correct}")

        if is_correct:
            results['correct'] += 1
            results['by_category'][category]['correct'] += 1
            results['by_should_answer'][answer_type]['correct'] += 1
            status = "PASS"
        else:
            results['incorrect'] += 1
            status = "FAIL"

        print(f"Статус: {status}")

        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'question': q['question'],
            'should_answer': q['should_answer'],
            'category': q['category'],
            'response_length': len(response),
            'sources': sources,
            'is_correct': is_correct,
            'status': status
        }
        logs.append(log_entry)

        with open(LOGS_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')

    print("\n" + "="*60)
    print(f"Результаты: {results['correct']}/{results['total']} правильных ({results['correct']/results['total']*100:.1f}%)")
    print("="*60)

    return results, logs


if __name__ == "__main__":
    if os.path.exists(LOGS_FILE):
        os.remove(LOGS_FILE)

    results, logs = run_evaluation()
    print(f"\nЛоги сохранены в {LOGS_FILE}")
