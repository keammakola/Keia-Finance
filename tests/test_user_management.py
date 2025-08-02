import pytest
import sqlite3
import bcrypt
from pathlib import Path
from src.user_management import create_account, login_account, get_db_connection, normalize_name
import tempfile

@pytest.fixture
def temp_db(tmp_path):
    db_path = tmp_path / "test_appdata.db"
    # Create the users table
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
    return str(db_path)


def test_normalize_name():
    assert normalize_name("john") == "John"
    assert normalize_name("mary-ann") == "Mary-Ann"
    assert normalize_name("o'connor") == "O'Connor"
    assert normalize_name("jean-luc picard") == "Jean-Luc Picard"


def test_create_account_success(temp_db):
    inputs = iter([
        "test@example.com",    # email
        "test user",           # name
    ])
    passwords = iter([
        "StrongPass1!",        # password
        "StrongPass1!"         # confirm
    ])
    outputs = []

    def fake_input(prompt=""):
        return next(inputs)

    def fake_getpass(prompt=""):
        return next(passwords)

    def fake_print(*args):
        outputs.append(" ".join(str(a) for a in args))

    result = create_account(
        db_path=temp_db,
        input_func=fake_input,
        getpass_func=fake_getpass,
        print_func=fake_print,
    )
    assert result is True
    assert any("Sweet! All done" in o for o in outputs)

    # Check user inserted in DB
    conn = get_db_connection(temp_db)
    cursor = conn.cursor()
    cursor.execute("SELECT email, name FROM users WHERE email = ?", ("test@example.com",))
    row = cursor.fetchone()
    conn.close()
    assert row is not None
    assert row[0] == "test@example.com"
    assert row[1] == "Test User"  # normalized


def test_create_account_email_taken(temp_db):
    # Insert an existing user
    conn = get_db_connection(temp_db)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (email, name, password) VALUES (?, ?, ?)",
                   ("taken@example.com", "Taken User", b"hashed"))
    conn.commit()
    conn.close()

    inputs = iter([
        "taken@example.com",  # email (taken)
    ])
    outputs = []

    def fake_input(prompt=""):
        return next(inputs)

    def fake_print(*args):
        outputs.append(" ".join(str(a) for a in args))

    result = create_account(
        db_path=temp_db,
        input_func=fake_input,
        getpass_func=lambda x: "DoesntMatter",
        print_func=fake_print,
    )
    assert result is False
    assert any("email’s taken" in o for o in outputs)


def test_login_account_success(temp_db):
    # Insert a user with known password hash
    password = "StrongPass1!"
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = get_db_connection(temp_db)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (email, name, password) VALUES (?, ?, ?)",
                   ("login@example.com", "Login User", hashed))
    conn.commit()
    conn.close()

    inputs = iter([
        "login@example.com",  # email
    ])
    passwords = iter([
        "StrongPass1!",      # correct password
    ])
    outputs = []

    def fake_input(prompt=""):
        return next(inputs)

    def fake_getpass(prompt=""):
        return next(passwords)

    def fake_print(*args):
        outputs.append(" ".join(str(a) for a in args))

    user = login_account(
        db_path=temp_db,
        input_func=fake_input,
        getpass_func=fake_getpass,
        print_func=fake_print,
    )
    assert user is not None
    assert user["email"] == "login@example.com"
    assert user["name"] == "Login User"
    assert any("Welcome back" in o for o in outputs)


def test_login_account_wrong_password(temp_db):
    password = "StrongPass1!"
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = get_db_connection(temp_db)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (email, name, password) VALUES (?, ?, ?)",
                   ("loginfail@example.com", "Login Fail", hashed))
    conn.commit()
    conn.close()

    inputs = iter([
        "loginfail@example.com",  # email
    ])
    passwords = iter([
        "WrongPass1!",
        "WrongPass2!",
        "WrongPass3!"
    ])
    outputs = []

    def fake_input(prompt=""):
        return next(inputs)

    def fake_getpass(prompt=""):
        return next(passwords)

    def fake_print(*args):
        outputs.append(" ".join(str(a) for a in args))

    user = login_account(
        db_path=temp_db,
        input_func=fake_input,
        getpass_func=fake_getpass,
        print_func=fake_print,
    )
    assert user is None
    assert any("too many tries" in o.lower() for o in outputs)


def test_login_account_email_not_found(temp_db):
    inputs = iter([
        "notfound@example.com",  # email
    ])
    outputs = []

    def fake_input(prompt=""):
        return next(inputs)

    def fake_print(*args):
        outputs.append(" ".join(str(a) for a in args))

    user = login_account(
        db_path=temp_db,
        input_func=fake_input,
        getpass_func=lambda x: "nope",
        print_func=fake_print,
    )
    assert user is None
    assert any("can’t find that email" in o.lower() for o in outputs)

