import sqlite3

conn = sqlite3.connect('../database.db')
cursor = conn.cursor()


# Создание таблицы для хранения настроек генерации изображений
def create_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Error(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        error TEXT,
        id_user INT
    );
    ''')
    conn.commit()

#  При отправке ошибки пользователем он должен будет написать только ошибку а данные с его id автоматически добавится
# и в БД сохранится ошибка и id пользователя, кто написал данную ошибку
# Добавление ID пользователя при его регистрации
def write_error(id_user, error):
    cursor.execute('INSERT INTO Error (id_user, error) VALUES (?, ?)', (id_user, error))
    conn.commit()

# Получить все ошибки
def get_all_error():
    cursor.execute('SELECT * FROM Error')
    conn.commit()
    data_error = cursor.fetchall()
    return data_error


# Удалить строку с ошибкой, на которую был дан ответ
def delete_error(id_error):
    cursor.execute('DELETE FROM Error WHERE ID = ?', (id_error,))
    conn.commit()
