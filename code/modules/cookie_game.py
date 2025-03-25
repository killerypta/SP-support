import asyncio
from aiogram import Router, types
from aiogram.filters import Command
from database import eat_cookie, get_top_cookie

router = Router()

@router.message(Command("cookie"))
async def cookie(message: types.Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name.replace("<", "&lt;").replace(">", "&gt;")  # Экранируем HTML
    user_link = f'<a href="tg://user?id={user_id}">{first_name}</a>'  # Гиперссылка на профиль

    # Проверка кулдауна
    weight, remaining_minutes, remaining_seconds = eat_cookie(user_id, first_name)

    # Отправляем сообщение с результатом
    if weight is None:
        # Если кулдаун не прошел, показываем сколько времени осталось
        result_message = await message.answer(f"{user_link}, повтори через <b>{remaining_minutes} минут</b> и <b>{remaining_seconds} секунд</b>.", parse_mode="HTML")
    else:
        # Если кулдаун прошел, печенька съедена
        result_message = await message.answer(f"{user_link}, ты съел(а) <b>{weight} кг</b> печенья 🍪 Съедено уже <b>{weight} кг</b>.", parse_mode="HTML")
    
    # Удаляем сообщение пользователя и бота через 15 секунд
    await asyncio.sleep(15)
    await message.delete()  # Удаляем сообщение пользователя
    await result_message.delete()  # Удаляем сообщение бота
                    
@router.message(Command("cookietop"))
async def cookie_top(message: types.Message):
    top_users = get_top_cookie()
    if not top_users:
        await message.answer("Топ пока пуст! Начни собирать печеньки /cookie! 🍪")
        return
    
    top_text = "🍪 <b>Топ 10</b> игроков <b>Cookie!</b> за все время:\n"
    for i, (user_id, first_name, total_weight) in enumerate(top_users):
        first_name = first_name.replace("<", "&lt;").replace(">", "&gt;")  # Экранируем HTML
        user_link = f'<a href="tg://user?id={user_id}">{first_name}</a>'  # Гиперссылка на профиль
        top_text += f"{i+1}. {user_link} — <b>{total_weight} кг</b>\n"

    await message.answer(top_text, parse_mode="HTML")
