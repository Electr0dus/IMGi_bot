import sqlite3

conn = sqlite3.connect('reg_user.db')
cursor = conn.cursor()


def create_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
        id_user INT PRIMARY KEY,
        username TEXT,
    );
    ''')
