import time
import random
import sqlite3

def create_db():
    conn = sqlite3.connect("DataBase.db")
    cursor = conn.cursor()
    
    # Таблица для чатов
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_id (
        id INTEGER PRIMARY KEY,
        banned BOOLEAN DEFAULT 0
    )
    """)

    # Таблица для печенек (cookie)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cookie (
        user_id INTEGER PRIMARY KEY,
        first_name TEXT,
        total_weight REAL DEFAULT 0,
        last_used INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()


def add_chat_id(chat_id):
    conn = sqlite3.connect("DataBase.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO chat_id (id) VALUES (?)", (chat_id,))
    conn.commit()
    conn.close()

def is_banned(chat_id):
    conn = sqlite3.connect("DataBase.db")
    cursor = conn.cursor()
    cursor.execute("SELECT banned FROM chat_id WHERE id = ?", (chat_id,))
    result = cursor.fetchone()
    conn.close()
    return result and result[0] == 1

def eat_cookie(user_id, first_name):
    conn = sqlite3.connect("DataBase.db")
    cursor = conn.cursor()

    # Получаем текущее время в секундах
    current_time = int(time.time())

    # Получаем информацию о пользователе
    cursor.execute("SELECT total_weight, last_used FROM cookie WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()

    # Если пользователь не найден в базе данных, создаем его запись
    if not row:
        weight = round(random.uniform(0.3, 5.0), 1)  # Генерируем случайный вес печеньки
        cursor.execute("""
            INSERT INTO cookie (user_id, first_name, total_weight, last_used)
            VALUES (?, ?, ?, ?)
        """, (user_id, first_name, weight, current_time))
        conn.commit()
        conn.close()
        return weight, None, None  # Возвращаем вес печеньки, так как это новый пользователь

    # Если пользователь найден, проверяем кулдаун
    total_weight, last_used = row
    if current_time - last_used < 1200:
        remaining_time = 1200 - (current_time - last_used)
        remaining_minutes = remaining_time // 60
        remaining_seconds = remaining_time % 60
        conn.close()
        return None, remaining_minutes, remaining_seconds

    # Если прошло больше 20 минут, обновляем данные
    weight = round(random.uniform(0.3, 5.0), 1)
    total_weight += weight
    cursor.execute("""
        INSERT INTO cookie (user_id, first_name, total_weight, last_used)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id) 
        DO UPDATE SET first_name = ?, total_weight = total_weight + ?, last_used = ?
    """, (user_id, first_name, weight, current_time, first_name, weight, current_time))

    conn.commit()
    conn.close()

    return weight, None, None

def get_top_cookie():
    conn = sqlite3.connect("DataBase.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, first_name, ROUND(total_weight, 1) FROM cookie ORDER BY total_weight DESC LIMIT 10")
    top_users = cursor.fetchall()
    conn.close()
    return top_users

def get_total_weight(user_id):
    conn = sqlite3.connect("DataBase.db")
    cursor = conn.cursor()
    cursor.execute("SELECT ROUND(total_weight, 1) FROM cookie WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return result[0]
    return 0  # Если пользователь не найден, возвращаем 0