# main.py
import asyncio
import sqlite3
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from config import TOKEN
from handlers import router
from database import create_db, add_chat_id, is_banned
from modules.rules import get_rule  # импортируем из modules/rules
from modules.cookie_game import router as cookie_router

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)
dp.include_router(cookie_router)

# Подключение к базе данных SQLite и создание таблиц, если они отсутствуют
create_db()

async def main():
    """Запускает бота с использованием polling."""
    print("Бот запускается...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
