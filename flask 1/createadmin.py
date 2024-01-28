import sqlite3

from werkzeug.security import generate_password_hash, check_password_hash
def create_user(name, email, psw):
    hashed_password = generate_password_hash(psw)
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (name, email, psw, is_admin) VALUES (?, ?, ?, ?)', (name, email, hashed_password, 1))
    conn.commit()
    conn.close()

create_user('Елизавета', 'admin@mail.ru', 'admin')
