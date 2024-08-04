import sqlite3

class Database:
    def __init__(self, path='data/lastfm.db'):
        self.conn = sqlite3.connect(path)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users 
                    (
                        id TEXT PRIMARY KEY,
                        username TEXT NOT NULL
                    )
                """
            )

    def link_account(self, id, username):
        with self.conn:
            self.conn.execute(
                """
                INSERT OR REPLACE INTO users 
                    (
                        id, 
                        username
                    )
                VALUES (?, ?)
                """, 
                (
                    id, 
                    username
                )
            )

    def get_username(self, id):
        cursor = self.conn.cursor()
        cursor.execute(
            '''
            SELECT username 
            FROM users 
            WHERE id = ?
            ''', 
            (id,)
        )
        row = cursor.fetchone()
        return row[0] if row else None