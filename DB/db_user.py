import sqlite3

conn = sqlite3.connect('../database.db')
cursor = conn.cursor()
cursor.execute('PRAGMA foreign_keys=ON')
conn.commit()

# Создание таблицы для хранения Регестрации пользователей
def create_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
        id_user INT PRIMARY KEY,
        username TEXT NOT NULL
    );
    ''')
    conn.commit()


# Добавить нового пользователя в таблицу Users
def create(id_tg, user):
    cursor.execute('INSERT INTO Users (id_user, username) VALUES (?, ?)', (id_tg, user))
    conn.commit()


# Функция проверки регестрации для предотвращения дублирования данными таблицы
# Возвращает False если пользователь уже есть
def check_users(id_user):
    cursor.execute('SELECT id_user FROM Users')
    all_id = cursor.fetchall()
    for id_ in all_id:
        for id_val in id_:
            if id_user == id_val:
                return False
    return True
