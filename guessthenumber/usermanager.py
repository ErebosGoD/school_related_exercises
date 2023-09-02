import sqlite3
from werkzeug.security import generate_password_hash


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
                username TEXT UNIQUE,
                password TEXT
                )''')

            self.connection.execute(''' CREATE TABLE IF NOT EXISTS scores (
                username TEXT PRIMARY KEY,
                score INTEGER 
                )''')

    def create_user(self, username, password):
        with self.connection:
            cursor = self.connection.execute('''
                SELECT username
                FROM users
                WHERE username = ?
            ''', (username,))

            existing_user = cursor.fetchone()

            if existing_user:
                raise ValueError("Benutzername bereits vorhanden")

            hashed_password = generate_password_hash(password, method='scrypt')
            self.connection.execute(
                '''INSERT INTO users (username, password) VALUES (?, ?)''', (username, hashed_password))

            self.connection.execute('''
                INSERT INTO scores (username, score)
                VALUES (?, ?)
            ''', (username, 1000))

    def update_score(self, new_score, username):
        with self.connection:
            # Holen Sie sich den aktuellen Score aus der Datenbank
            cursor = self.connection.execute('''
                SELECT score
                FROM scores
                WHERE username = ?
            ''', (username,))
            current_score = cursor.fetchone()

            # Wenn es keinen aktuellen Score gibt oder der neue Score höher ist, aktualisieren Sie ihn
            if not current_score or new_score > current_score[0]:
                self.connection.execute('''
                    UPDATE scores
                    SET score = ?
                    WHERE username = ?
                ''', (new_score, username))

    def get_user(self, username):
        with self.connection:
            cursor = self.connection.execute('''
                SELECT username, password
                FROM users
                WHERE username = ?
            ''', (username,))

            row = cursor.fetchone()
            if row:
                user = {
                    'username': row[0],
                    'password': row[1]
                }
                return user
            return None

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
