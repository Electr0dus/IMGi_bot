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
        username TEXT
    );
    ''')
    conn.commit()



# Сохранить имя сгенерированного фото с id пользователем
def save_image_rating(id_user: int, name_photo: str, username: str):
    cursor.execute('INSERT INTO Rating (id_user, name_photo, username) VALUES (?, ?, ?)',
                   (id_user, name_photo, username))
    conn.commit()
