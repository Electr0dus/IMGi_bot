import sqlite3

conn = sqlite3.connect('../database.db')
cursor = conn.cursor()


# Создание таблицы для хранения настроек генерации изображений
def create_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Error(
        error TEXT,
        id_user INT PRIMARY KEY,
        FOREIGN KEY (id_user) REFERENCES Users(id_user)
    );
    ''')
    conn.commit()

# Добавление ID пользователя при его регистрации
def create_user_id(id_tg):
    cursor.execute('INSERT INTO Error (id_user) VALUES (?)', (id_tg,))
    conn.commit()
