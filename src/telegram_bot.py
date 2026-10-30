import os
import sys
import logging
import asyncio
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except ImportError:
    pass

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rag_bot import RAGBot
from config import MAX_QUERY_LENGTH

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN not set. Create .env file from .env.example.")
KNOWLEDGE_INDEX = os.getenv("KNOWLEDGE_INDEX", "faiss.index")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

rag_bot = None


def get_rag_bot():
    global rag_bot
    if rag_bot is None:
        rag_bot = RAGBot(enable_security=True)
    return rag_bot


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я RAG-бот по базе знаний Quantum Realms.\n"
        "Задайте мне вопрос, и я найду ответ в базе знаний."
    )


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "Доступные команды:\n"
        "/start - Начать диалог\n"
        "/help - Показать справку\n"
        "\n"
        "Просто отправьте мне вопрос, и я постараюсь найти ответ в базе знаний."
    )


@dp.message(lambda message: message.photo or message.video or message.audio or message.voice or message.sticker or message.animation)
async def handle_media(message: types.Message):
    await message.answer("Я понимаю только текстовые сообщения. Пожалуйста, задайте вопрос текстом.")


@dp.message()
async def handle_message(message: types.Message):
    user_query = message.text.strip()
    if not user_query:
        return

    if len(user_query) > MAX_QUERY_LENGTH:
        await message.answer(f"Ваш запрос слишком длинный. Пожалуйста, задайте вопрос короче (максимум {MAX_QUERY_LENGTH} символов).")
        return

    await message.answer_chat_action("typing")

    try:
        rag = get_rag_bot()
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, rag.ask, user_query)

        if len(response) > 4096:
            response = response[:4093] + "..."

        await message.answer(response)
    except Exception as e:
        logger.exception(f"Error processing query: {user_query}")
        await message.answer("Извините, произошла ошибка при обработке вашего запроса.")


async def main():
    logger.info("Запуск Telegram-бота...")

    try:
        await dp.start_polling(bot)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен пользователем")
    finally:
        await graceful_shutdown()


async def graceful_shutdown():
    try:
        await bot.session.close()
    except Exception:
        pass
    finally:
        loop = asyncio.get_event_loop()
        loop.stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен")
