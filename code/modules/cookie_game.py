import asyncio
from aiogram import Router, types
from aiogram.filters import Command
from service.database import eat_cookie, get_top_cookie, get_total_weight
from service.utils import escape_html, get_user_info

router = Router()

@router.message(Command("cookie"))
async def cookie(message: types.Message):
    user_id, first_name = get_user_info(message)
    # Проверка кулдауна
    weight, remaining_minutes, remaining_seconds = eat_cookie(user_id, first_name)

    total_weight = get_total_weight(user_id)

    if weight is None:
        result_message = await message.answer(f"<code>{first_name}</code>, повтори через <b>{remaining_minutes} минут</b> и <b>{remaining_seconds} секунд</b>.", parse_mode="HTML")
    else:
        result_message = await message.answer(f"<code>{first_name}</code>, ты съел(а) <b>{weight} кг</b> печенья 🍪 Съедено уже <b>{total_weight} кг</b>.", parse_mode="HTML")
    
    # Автоудаление сообщения через 60 секунд 
    await asyncio.sleep(60)
    await message.delete()
    await result_message.delete()
                    
@router.message(Command("cookietop"))
async def cookie_top(message: types.Message):
    top_users = get_top_cookie()
    if not top_users:
        await message.answer("Топ пока пуст! Начни собирать печеньки /cookie! 🍪")
        return
    
    top_text = "🍪 <b>Топ 10</b> игроков <b>Cookie!</b> за все время:\n"
    for i, (user_id, first_name, total_weight) in enumerate(top_users):
        top_text += f"{i+1}. <code>{first_name}</code> — <b>{total_weight} кг</b>\n"

    result_message = await message.answer(top_text, parse_mode="HTML")

    # Автоудаление сообщения через 180 секунд
    await asyncio.sleep(180)
    await message.delete()
    await result_message.delete()