import os
import sqlite3

def create_db(base_dir='userdata'):
    os.makedirs(base_dir, exist_ok=True)
    db_path = os.path.join(base_dir, 'appdata.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        password BLOB NOT NULL,
        created_at TIMESTAMP,
        last_login TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()
    return db_path  # return path for testing convenience
