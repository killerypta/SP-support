from aiogram import types

# Экранирование HTML
def escape_html(text: str) -> str:
    return text.replace("<", "&lt;").replace(">", "&gt;")

# Получение информации о пользователе
def get_user_info(message: types.Message) -> tuple[int, str]:
    user_id = message.from_user.id
    first_name = escape_html(message.from_user.first_name)
    return user_id, first_name
