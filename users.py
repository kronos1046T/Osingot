import db
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

def get_user(user_id):
    sql = """ SELECT id, username 
            FROM users 
            WHERE id = ? 
        """
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_positions_by_user(user_id):
    sql = """ SELECT id, stock_name
            FROM positions 
            WHERE user_id = ? 
            ORDER BY id DESC
        """
    return db.query(sql, [user_id])

def create_user(username, password1, password2):
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"

    password_hash = generate_password_hash(password1)

    try:
        sql = """
            INSERT INTO users (username, password_hash)
            VALUES (?, ?)
        """
        db.execute(sql, [username, password_hash])

    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"


def login_user(username, password):
    sql = """
        SELECT id, username, password_hash
        FROM users
        WHERE username = ?
    """

    result = db.query(sql, [username])

    if not result:
        return None  # user not found

    user_id, username, password_hash = result[0]

    if check_password_hash(password_hash, password):
        return {
            "id": user_id,
            "username": username
        }

    return None