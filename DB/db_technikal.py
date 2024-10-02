import sqlite3

conn = sqlite3.connect('../database.db')
cursor = conn.cursor()


# Создание таблицы для хранения настроек генерации изображений
def create_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Technical(
        id_user INT,
        prompt TEXT,
        name_file TEXT
    );
    ''')
    conn.commit()


# Создать таблицу при регистрации пользователя
def create_user(id_user):
    cursor.execute('INSERT INTO Technical (id_user) VALUES (?)',
                   (id_user,))
    conn.commit()

# Добавить технические данные в БД
def creat_data_tech(id_user: int, prompt: str, name_file: str):
    cursor.execute('UPDATE Technical SET prompt = ?, name_file = ? WHERE id_user = ?',
                   (prompt, name_file, id_user))
    conn.commit()

# Получить данные для повторной генерации фото
def get_tech_data(id_user: int):
    cursor.execute('SELECT prompt, name_file FROM Technical WHERE id_user = ?', (id_user,))
    conn.commit()
    data = cursor.fetchall()
    return data[0] #Здесь ошибка убрать индекс [0]

# Удалить техническую информацию из БД пользователя по id
def delete_data_tech(id_user: int):
    cursor.execute('UPDATE Technical SET prompt = ?, name_file = ? WHERE id_user = ?', (None, None, id_user,))
    conn.commit()