import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()


# Создание таблицы для хранения настроек генерации изображений
def create_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Error(
        name_user TEXT,
        error TEXT
    );
    ''')
    conn.commit()
