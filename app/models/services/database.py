import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database.db"

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.create_tables()
        
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                gender TEXT,
                birth_date TEXT,
                comments TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
        
    def execute_query(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor.lastrowid
    
    def fetch_all(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
    
    def __del__(self):
        self.conn.close()