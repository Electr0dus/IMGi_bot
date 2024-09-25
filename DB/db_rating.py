import sqlite3

conn = sqlite3.connect('../database.db')
cursor = conn.cursor()
cursor.execute('PRAGMA foreign_keys=ON')
conn.commit()


# Создание таблицы для хранения настроек генерации изображений
def create_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Rating(
        name_photo TEXT,
        like INT DEFAULT 0,
        id_user INT,
        username TEXT,
        FOREIGN KEY (id_user) REFERENCES Users(id_user)
    );
    ''')
    conn.commit()
# FOREIGN KEY (name_photo) REFERENCES Photo(name_photo)
def create_user_id(id_tg, username):
    cursor.execute('INSERT INTO Rating (id_user, username) VALUES (?, ?)', (id_tg, username))
    conn.commit()