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


#Получить текущее значение лайков
def get_like_current(id_user, name_photo):
    cursor.execute('SELECT like FROM Rating WHERE id_user = ? AND name_photo = ?', (id_user, name_photo))
    conn.commit()
    data = cursor.fetchone()[0]
    return data

# Записать новое значение лайков
def send_like_image(id_user, name_photo, like):
    cursor.execute('UPDATE Rating SET like = ? WHERE id_user = ? AND name_photo = ?', (like, id_user, name_photo,))
    conn.commit()