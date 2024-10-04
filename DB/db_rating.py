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

# Получить максимальное значение в таблице лайков. Указав в параметр 0 - первое место 1 - второе место 2 - третье место
def get_max_like(sw_place: int):
    '''
    Логика работы: делаем запррос на получение максимального значения лайков и групируем все эти значения в одно
    в порядке убывания из полученных данных нужны будут только три первых параметра это соответственно первое второе и третье место
    затем запрашиваем из таблицы все строки где лайки равны соответствующиму числу и возвращаем все полученные строки
    для вывода их пользователю
    :param sw_place: Место которое необходимо получить 1, 2, 3
    :return: список параметров для вывода пользователю изображения
    '''
    # Отсортировать по уменьшению лайков
    cursor.execute('SELECT * FROM Rating GROUP BY like ORDER BY like DESC')
    conn.commit()
    data_max_like = cursor.fetchall()
    # data_max_like[0] - первое место
    # data_max_like[1] - второе место
    # data_max_like[2] - третье место
    # Для первого места
    print(data_max_like)
    if sw_place == 1:
        cursor.execute('SELECT * FROM Rating WHERE like = ?', (data_max_like[0][1],))
        data_first = cursor.fetchall()
        return data_first
    # Для второго места
    elif sw_place == 2:
        cursor.execute('SELECT * FROM Rating WHERE like = ?', (data_max_like[1][1],))
        data_first = cursor.fetchall()
        return data_first
    # Для третьего места
    elif sw_place == 3:
        cursor.execute('SELECT * FROM Rating WHERE like = ?', (data_max_like[2][1],))
        data_first = cursor.fetchall()
        return data_first

