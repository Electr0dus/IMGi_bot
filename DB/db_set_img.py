import sqlite3

conn = sqlite3.connect('../database.db')
cursor = conn.cursor()
cursor.execute('PRAGMA foreign_keys=ON')
conn.commit()


# Создание таблицы для хранения настроек генерации изображений
def create_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Settings(
        style_img TEXT DEFAULT "DEFAULT",
        negative_prompt TEXT DEFAULT None,
        width INT DEFAULT 1024,
        height INT DEFAULT 1024,
        preset INT DEFAULT 0,
        id_user INT PRIMARY KEY,
        FOREIGN KEY (id_user) REFERENCES Users(id_user)
    );
    ''')
    conn.commit()

# Получить данные настройки запроса для пользователя
def get_set_user(id_user):
    cursor.execute('SELECT * FROM Settings WHERE id_user = ?', (id_user,))
    conn.commit()
    data: list = cursor.fetchall()
    return data

# Добавление ID пользователя при его регистрации
def create_user_id(id_tg):
    cursor.execute('INSERT INTO Settings (id_user) VALUES (?)', (id_tg,))
    conn.commit()


# Установить стиль генерации для конкретного пользователя
def set_style_user(id_user, style):
    cursor.execute('UPDATE Settings SET style_img = ? WHERE id_user = ?', (style, id_user))
    conn.commit()
