import sqlite3


class UserManager:
    def __init__(self, database_path) -> None:
        self.connection = sqlite3.connect(
            database_path, check_same_thread=False)
        self._create_tables()

    def close(self):
        self.connection.close()

    def _create_tables(self):
        with self.connection:
            self.connection.execute(''' CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE
                )''')

            self.connection.execute(''' CREATE TABLE IF NOT EXISTS scores (
                username TEXT PRIMARY KEY,
                score INTEGER 
                )''')

    def create_user(self, username):
        with self.connection:
            cursor = self.connection.execute('''
                SELECT username
                FROM users
                WHERE username = ?
            ''', (username,))

            existing_user = cursor.fetchone()

            if existing_user:
                raise ValueError("User already exists")

            self.connection.execute(
                ''' INSERT INTO users (username) VALUES (?)''', (username,))

            self.connection.execute('''
                INSERT INTO scores (username, score)
                VALUES (?, ?)
            ''', (username, 1000))

    def update_score(self, score, username):
        with self.connection:
            self.connection.execute('''
                UPDATE scores
                SET score = ?
                WHERE username = ?
            ''', (score, username))

    def get_score(self, username):
        with self.connection:
            cursor = self.conn.execute('''
                SELECT score
                FROM scores
                WHERE username = ?
            ''', (username,))
            row = cursor.fetchone()
            if row:
                return row[0]
            return None
