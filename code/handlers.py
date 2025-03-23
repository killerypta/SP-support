# handlers.py
from aiogram import Router, F
from aiogram.types import Message
from database import add_chat_id, is_banned
from modules.rules import get_rule  # импортируем из modules/rules

router = Router()

@router.message(F.text.in_(["/start", "/help"]))
async def send_welcome(message: Message):
    # Регистрация chat_id в базе данных
    add_chat_id(message.chat.id)

    await message.answer(
        "<b>🛠 <a href=\"https://t.me/BETA_Sapphire_Palace_support_bot\">Sapphire Palace support | Бот поддержки</a> приветствует Вас!</b>\n"
        "Я могу предложить следующие темы:\n\n"
        "<b>1)</b><i>*В процессе</i>\n"
        "<b>2)</b><i>*В процессе</i>\n"
        "<b>3)</b><i>*В процессе</i>\n"
        "<b>4)</b><i>*В процессе</i>\n"
        "<b>5)</b><i>*В процессе</i>\n\n"
        "<b>👨‍💻 Агенты поддержки</b>, которые могут ответить на Ваши вопросы: @killerypta\n\n"
        "🗂 Список всех команд <a href=\"https://teletype.in/@killerypta/SP-support-commands\">с их описанием</a>.\n"
        "📢 Официальный <a href=\"https://github.com/killerypta/SP-support\">репозиторий</a> бота.",
        parse_mode="HTML",
        disable_web_page_preview=True
    )

@router.message(F.text.lower() == "команды")
async def send_commands(message: Message):
    await message.answer(
        "⚙️ Полный список команд в <a href=\"https://teletype.in/@killerypta/SP-support-commands\">нашей статье</a>",
        parse_mode="HTML"
    )

@router.message(F.text.startswith("!"))
async def send_rule(message: Message):
    # Проверка на бан
    if is_banned(message.chat.id):
        await message.answer("Вы заблокированы и не можете использовать бота.")
        return
    
    # Получение правила по команде
    rule = get_rule(message.text.strip())
    await message.answer(rule)
