import os.path
import sqlite3

class Database:
    def __init__(self):
        self.db_file = os.path.join(os.getcwd(), 'database.db')
        self.init_db()

    def get_db(self):
        connect = sqlite3.connect(self.db_file, check_same_thread=False)
        return connect

    def init_db(self):
        db = self.get_db()
        cursor = db.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            cum INTEGER NOT NULL,
            sex INTEGER NOT NULL
        )
        ''')
        db.commit()
        db.close()

    def get_user(self, id):
        db = self.get_db()
        cursor = db.cursor()
        user = cursor.execute(f'''SELECT * FROM users WHERE id = {id}''').fetchone()
        db.commit()
        db.close()
        return user

    def set_user(self, message):
        db = self.get_db()
        cursor = db.cursor()
        user = self.get_user(message.from_user.id)
        if user is not None:
            return f'ℹ️ <a href="tg://user?id={user[0]}">{user[1]}</a> уже зарегистрирован'
        cursor.execute(
            '''INSERT INTO users VALUES (?, ?, ?, ?)''',
            (message.from_user.id,
             message.from_user.first_name if message.from_user.username is None else message.from_user.username, 0, 0)).fetchone()
        db.commit()
        db.close()
        user = self.get_user(message.from_user.id)
        return f'✅ <a href="tg://user?id={user[0]}">{user[1]}</a> зарегистрирован'

    def update_user(self, new_user):
        db = self.get_db()
        cursor = db.cursor()
        user = self.get_user(new_user[0])
        if user is None:
            return f'⚠️ Вы не зарегистрированы'
        else:
            cursor.execute(
                '''UPDATE users SET name = ?, cum = ?, sex = ? WHERE id = ?''',
                (new_user[1], new_user[2], new_user[3], new_user[0]))
            db.commit()
            db.close()
            return f'✅ Пользователь обновлен'
