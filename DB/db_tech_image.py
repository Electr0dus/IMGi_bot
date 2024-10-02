import sqlite3

conn = sqlite3.connect('../database.db')
cursor = conn.cursor()


# Создание таблицы для хранения настроек генерации изображений
def create_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Tech_image(
        id_user INT,
        current_image TEXT,
        current_number_img INT DEFAULT 0
    );
    ''')
    conn.commit()

# Создать пользователя в таблице при регистрации пользователей
def create_user_im(id_user):
    cursor.execute('INSERT INTO Tech_image (id_user) VALUES (?)',
                   (id_user,))
    conn.commit()

# Добавить выбранное изображение для просмотра
def add_current_image(id_user, current_image):
    cursor.execute('UPDATE Tech_image SET current_image = ? WHERE id_user = ?',
                   (current_image, id_user))
    conn.commit()

# Получить текущий файл пользователя для сохранения на устройство
def get_current_image(id_user):
    cursor.execute('SELECT current_image FROM Tech_image WHERE id_user = ?', (id_user,))
    conn.commit()
    data = cursor.fetchall()
    return data[0]

# Получить текущнн значение номера изображения
def get_current_number(id_user):
    cursor.execute('SELECT current_number_img FROM Tech_image WHERE id_user = ?', (id_user,))
    conn.commit()
    data = cursor.fetchone()[0]
    return data


# Записать новое значение для просомтра изображений всех пользователей
def add_current_number(id_user, current_number_img):
    cursor.execute('UPDATE Tech_image SET current_number_img = ? WHERE id_user = ?',
                   (current_number_img, id_user))
    conn.commit()
