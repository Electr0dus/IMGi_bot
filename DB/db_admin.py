import sqlite3

conn = sqlite3.connect('../database.db')
cursor = conn.cursor()


# Создание таблицы для админ панели
def create_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Admin(
        id_user INT,
        password TEXT
    );
    ''')
    conn.commit()

#  Добавить админа
def add_user_to_admin(id_user, password: str):
    cursor.execute('INSERT INTO Admin (id_user, password) VALUES (?, ?)', (id_user, password))
    conn.commit()

# Проверить, что пользователь является админом
def check_user_admin(id_user: int, password: str):
    cursor.execute('SELECT * FROM Admin WHERE id_user = ?', (id_user,))
    conn.commit()
    data_admin = cursor.fetchall()
    # Если пустой список, значит такого пользователя нет вернуть при этом 1
    # Если данный пользователь есть, а пароль не верный то вернуть 2
    # Если все проверки пройдены то вернуть 3
    if len(data_admin) == 0:
        return 1
    else:
        for admin in data_admin:
            if id_user == admin[0]:
                if password == admin[1]:
                    return 3
        return 2

# Удалить админку у пользователя
def delete_admin(id_user):
    cursor.execute('DELETE FROM Admin WHERE id_user = ?', (id_user,))
    conn.commit()

# Получить список всех пользователей
def get_all_admin():
    cursor.execute('SELECT * FROM Admin')
    conn.commit()
    data = cursor.fetchall()
    return data
