import sqlite3
import os
from flask_login import UserMixin

DB_NAME = 'expenses.db'

class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    @staticmethod
    def get(user_id):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('SELECT id, username, password FROM users WHERE id = ?', (user_id,))
        user = c.fetchone()
        conn.close()
        if user:
            return User(*user)
        return None

    @staticmethod
    def get_by_username(username):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('SELECT id, username, password FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()
        if user:
            return User(*user)
        return None

def init_db():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )''')
        c.execute('''CREATE TABLE expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )''')
        c.execute('''CREATE TABLE budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            month TEXT NOT NULL,
            UNIQUE(user_id, category, month),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )''')
        c.execute('''CREATE TABLE incomes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            month TEXT NOT NULL,
            category TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )''')
        conn.commit()
        conn.close() 