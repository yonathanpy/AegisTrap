import sqlite3

class Database:
    def __init__(self, db_name="aegis.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.setup()

    def setup(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            username TEXT,
            password TEXT,
            command TEXT,
            timestamp TEXT
        )
        """)
        self.conn.commit()

    def insert(self, ip, username, password, command, timestamp):
        self.cursor.execute("""
        INSERT INTO sessions (ip, username, password, command, timestamp)
        VALUES (?, ?, ?, ?, ?)
        """, (ip, username, password, command, timestamp))
        self.conn.commit()
