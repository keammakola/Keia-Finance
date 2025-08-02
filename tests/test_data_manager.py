import os
import sqlite3
import tempfile
from src.data_manager import create_db

def test_create_db_creates_file_and_users_table():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = create_db(base_dir=tmpdir)

        assert os.path.isfile(db_path), "Database file was not created"

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
        result = cursor.fetchone()

        conn.close()

        assert result is not None, "'users' table was not created"
