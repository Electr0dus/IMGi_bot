import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('PRAGMA foreign_keys=ON')
conn.commit()


# Создание таблицы для хранения настроек генерации изображений
def create_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Rating(
        name_user TEXT,
        name_photo TEXT,
        like INT DEFAULT 0,
        FOREIGN KEY (name_user) REFERENCES Photo(name_user),
        FOREIGN KEY (name_photo) REFERENCES Photo(name_photo)
    );
    ''')
    conn.commit()