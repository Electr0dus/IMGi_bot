import sqlite3

conn = sqlite3.connect('../database.db')
cursor = conn.cursor()


# Создание таблицы для хранения настроек генерации изображений
def create_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Tech_image(
        id_user INT,
        current_image TEXT
    );
    ''')
    conn.commit()

# Создать пользователя в таблице при регистрации пользователей
def create_user_im(id_user):
    cursor.execute('INSERT INTO Tech_image (id_user) VALUES (?)',
                   (id_user,))
    conn.commit()
