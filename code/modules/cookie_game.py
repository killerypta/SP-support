# modules/cookie.py
import random
from database import update_cookie, get_cookietop

COOKIE_DATA = {}  # хранит общее количество съеденого печенья для каждого пользователя

def handle_cookie(username):
    """Обработка съеденного печенья пользователем"""
    # Генерируем случайное количество печенья от 0.3 до 3 кг
    weight = round(random.uniform(0.3, 3), 2)
    total = COOKIE_DATA.get(username, 0) + weight
    COOKIE_DATA[username] = total
    # Обновляем данные в БД
    update_cookie(username, weight)
    profile_link = f"<a href='https://example.com/user/{username}'>{username}</a>"
    print(f"{profile_link}, ты съел(а) {weight} кг печенья 🍪 Съедено уже {round(total, 2)}кг")

def handle_cookietop():
    """Получаем топ 10 игроков по съеденному печенью"""
    top_players = get_cookietop()
    for rank, (username, total) in enumerate(top_players, start=1):
        profile_link = f"<a href='https://example.com/user/{username}'>{username}</a>"
        print(f"{rank}. {profile_link} - {round(total, 2)}кг")
