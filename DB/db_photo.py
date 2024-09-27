import sqlite3

conn = sqlite3.connect('../database.db')
cursor = conn.cursor()
cursor.execute('PRAGMA foreign_keys=ON')
conn.commit()


# Создание таблицы для хранения настроек генерации изображений
def create_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Photo(
        name_photo TEXT,
        id_user INT PRIMARY KEY,
        FOREIGN KEY (id_user) REFERENCES Users(id_user)
    );
    ''')
    conn.commit()


# Добавление ID пользователя при его регистрации
def create_user_id(id_tg):
    cursor.execute('INSERT INTO Photo (id_user) VALUES (?)', (id_tg,))
    conn.commit()


# Найти файл с фото по id_user, если такое есть в базе, вернёт False, если нет - True
def check_photo(name_photo: str, id_name: int):
    cursor.execute('SELECT name_photo FROM Photo WHERE id_user = ?', (id_name,))
    conn.commit()
    all_photo = cursor.fetchall()
    for photo_list in all_photo:
        for photo in photo_list:
            if name_photo == photo:
                return False
    return True

# Получить имена фото конкретного пользователя
def get_all_photo(id_name: int):
    cursor.execute('SELECT name_photo FROM Photo WHERE id_user = ?', (id_name,))
    conn.commit()
    all_photo = cursor.fetchall()
    return all_photo[0]
