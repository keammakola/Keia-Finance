import re
import sqlite3
import bcrypt
from getpass import getpass
from datetime import datetime
import time

DEFAULT_DB_PATH = "userdata/appdata.db"


def get_db_connection(db_path=DEFAULT_DB_PATH):
    return sqlite3.connect(db_path)


def normalize_name(name: str) -> str:
    # Capitalize first letter of each part, keep apostrophes and hyphens
    def cap_word(word: str) -> str:
        if "'" in word:
            parts = word.split("'")
            return "'".join(part.capitalize() for part in parts)
        if "-" in word:
            parts = word.split("-")
            return "-".join(part.capitalize() for part in parts)
        return word.capitalize()

    return " ".join(cap_word(w) for w in name.split())


def is_valid_email(email: str) -> bool:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


def password_strength_issues(password: str) -> list[str]:
    issues = []
    if len(password) < 8:
        issues.append("at least 8 characters")
    if not re.search(r'[A-Z]', password):
        issues.append("an uppercase letter")
    if not re.search(r'[a-z]', password):
        issues.append("a lowercase letter")
    if not re.search(r'\d', password):
        issues.append("a number")
    if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
        issues.append("a special character")
    return issues


def create_account(
    db_path=DEFAULT_DB_PATH,
    input_func=input,
    getpass_func=getpass,
    print_func=print,
) -> bool:
    print_func("\nHey! Let's get you set up with a new account.")

    while True:
        email = input_func("Shoot me your email: ").strip().lower()
        if not is_valid_email(email):
            print_func("Hmm, that doesn’t look like a real email. Try again.")
            time.sleep(1.5)
            continue

        with get_db_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM users WHERE email = ?", (email,))
            if cursor.fetchone():
                print_func("Oops! That email’s taken. Try logging in instead?")
                return False
        break

    name_input = input_func("What should I call you? ").strip()
    name = normalize_name(name_input)

    attempts = 3
    while attempts > 0:
        password = getpass_func("Pick a password (don’t worry, it’s safe with me): ")
        issues = password_strength_issues(password)
        if issues:
            print_func("That password needs:", ", ".join(issues))
            time.sleep(1.5)
            continue

        confirm = getpass_func("Just making sure, type it again: ")
        if password != confirm:
            attempts -= 1
            if attempts > 0:
                print_func(f"Hmm, those passwords don’t match. Try again ({attempts} tries left).")
            else:
                print_func("Ah, too many mismatches. Let's try this later.")
                return False
            continue

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        with get_db_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (email, name, password, created_at) VALUES (?, ?, ?, ?)",
                (email, name, hashed, datetime.utcnow())
            )
            conn.commit()
        print_func(f"Sweet! All done, {name}. You’re good to go. Time to log in!")
        time.sleep(3)
        return True


def login_account(
    db_path=DEFAULT_DB_PATH,
    input_func=input,
    getpass_func=getpass,
    print_func=print,
) -> dict | None:
    print_func("\nWelcome back! Let’s get you logged in.")
    email = input_func("Your email: ").strip().lower()

    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, password FROM users WHERE email = ?", (email,))
        result = cursor.fetchone()

        if not result:
            print_func("Can’t find that email around here. You sure you signed up?")
            return None

        user_id, name, stored_hash = result

    attempts = 3
    while attempts > 0:
        password = getpass_func("Your secret password: ").encode('utf-8')
        if bcrypt.checkpw(password, stored_hash):
            print_func(f"Boom! Welcome back, {name} 👋")

            # Update last_login timestamp
            with get_db_connection(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE users SET last_login = ? WHERE id = ?",
                    (datetime.utcnow(), user_id)
                )
                conn.commit()

            # Return user info for session tracking
            return {"id": user_id, "name": name, "email": email}
        else:
            attempts -= 1
            if attempts > 0:
                print_func(f"Ahh, that password’s off. Try again ({attempts} tries left).")
                time.sleep(1.5)
            else:
                print_func("Dang, too many tries. Better luck next time!")
                return None


def reset_password(
    db_path=DEFAULT_DB_PATH,
    input_func=input,
    getpass_func=getpass,
    print_func=print,
) -> bool:
    print_func("\nForgot your password? No worries, let’s fix that.")
    email = input_func("Enter your email: ").strip().lower()

    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM users WHERE email = ?", (email,))
        result = cursor.fetchone()

        if not result:
            print_func("Hmm, we don’t have that email on file.")
            return False

        user_id, name = result

    attempts = 3
    while attempts > 0:
        new_password = getpass_func(f"{name}, pick a new password: ")
        issues = password_strength_issues(new_password)
        if issues:
            print_func("That password needs:", ", ".join(issues))
            time.sleep(1.5)
            continue

        confirm = getpass_func("Type it again to confirm: ")
        if new_password != confirm:
            attempts -= 1
            if attempts > 0:
                print_func(f"Passwords don’t match. Try again ({attempts} tries left).")
            else:
                print_func("Too many tries, please try resetting later.")
                return False
            continue

        hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        with get_db_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET password = ? WHERE id = ?",
                (hashed, user_id)
            )
            conn.commit()
        print_func("Nice! Your password’s been reset. You can log in now.")
        return True
