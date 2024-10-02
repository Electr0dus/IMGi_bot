import sqlite3

conn = sqlite3.connect('../database.db')
cursor = conn.cursor()


# Создание таблицы для хранения настроек генерации изображений
def create_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS CheckLike(
        current_user INT,
        liked_user INT,
        name_file_like TEXT
    );
    ''')
    conn.commit()


# Добавить кто лайкнул и кого лайкнули для отслеживания
def add_like_image(current_user, liked_user, name_file_like):
    cursor.execute('INSERT INTO CheckLike (current_user, liked_user, name_file_like) VALUES (?, ?, ?)',
                   (current_user, liked_user, name_file_like))
    conn.commit()


# Проверить, сделал ли пользователь лайк фото конкретного пользователя
def check_like_image(current_user, liked_user, name_file_like):
    cursor.execute('SELECT liked_user, name_file_like FROM CheckLike WHERE current_user = ?',
                   (current_user,))
    conn.commit()
    current_like = (liked_user, name_file_like)
    data = cursor.fetchall()
    for data_image in data:
        if current_like == data_image:
            return False
    return True
