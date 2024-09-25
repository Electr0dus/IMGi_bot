import sqlite3

conn = sqlite3.connect('../database.db')
cursor = conn.cursor()
cursor.execute('PRAGMA foreign_keys=ON')
conn.commit()


# Создание таблицы для хранения настроек генерации изображений
def create_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Settings(
        style_img TEXT,
        negative_prompt TEXT,
        width INT,
        height INT,
        preset TEXT,
        is_preset BOOLEAN NOT NULL DEFAULT 1,
        id_user INT PRIMARY KEY,
        FOREIGN KEY (id_user) REFERENCES Users(id_user)
    );
    ''')
    conn.commit()


# Добавление ID пользователя при его регистрации
def create_user_id(id_tg):
    cursor.execute('INSERT INTO Settings (id_user) VALUES (?)', (id_tg,))
    conn.commit()
