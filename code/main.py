# main.py
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from config import TOKEN
from handlers import router
from database import create_db
from modules.cookie_game import handle_cookie, handle_cookietop  # Импортируем обработку команд для печенья
from modules.rules import get_rule

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)

# Команды для миниигры "cookie"
@router.message(commands=["cookie"])
async def cookie_command(message: Message):
    handle_cookie(message.from_user.username)
    await message.answer(f"Ты съел(а) печенья! 🍪")

@router.message(commands=["cookietop"])
async def cookietop_command(message: Message):
    handle_cookietop()
    await message.answer("Вот топ 10 игроков по съеденному печенью!")

# Подключение к базе данных SQLite и создание таблиц, если они отсутствуют
create_db()

# Основная асинхронная функция для запуска бота
async def main():
    """Запускает бота с использованием polling."""
    print("Бот запускается...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
