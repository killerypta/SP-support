# database.py
import sqlite3

# Секция 1: Общие операции с базой данных (chat_ids)
def create_db():
    """Создает базу данных и таблицу для chat_ids."""
    conn = sqlite3.connect("DataBase.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_ids (
        id INTEGER PRIMARY KEY,
        banned BOOLEAN DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()

def add_chat_id(chat_id):
    """Добавляет новый chat_id в базу данных, если его нет."""
    conn = sqlite3.connect("DataBase.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO chat_ids (id) VALUES (?)", (chat_id,))
    conn.commit()
    conn.close()

def is_banned(chat_id):
    """Проверяет, заблокирован ли чат."""
    conn = sqlite3.connect("DataBase.db")
    cursor = conn.cursor()
    cursor.execute("SELECT banned FROM chat_ids WHERE id = ?", (chat_id,))
    result = cursor.fetchone()
    conn.close()
    return result and result[0] == 1


# Секция 2: Интеграция мини-игры (Cookie Game)
def init_cookie_game_db():
    """Создает таблицу для игры с печеньем, если ее нет."""
    conn = sqlite3.connect("DataBase.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Cookie (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nickname TEXT UNIQUE,
        eaten REAL DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()

def update_cookie(username, weight):
    """Обновляет количество съеденного печенья для пользователя."""
    conn = sqlite3.connect("DataBase.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO Cookie (nickname, eaten) VALUES (?, ?)", (username, 0))
    cursor.execute("UPDATE Cookie SET eaten = eaten + ? WHERE nickname = ?", (weight, username))
    conn.commit()
    conn.close()

def get_cookietop():
    """Получает топ 10 игроков по съеденному печенью из БД."""
    conn = sqlite3.connect("DataBase.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nickname, eaten FROM Cookie ORDER BY eaten DESC LIMIT 10")
    top_players = cursor.fetchall()
    conn.close()
    return top_players
