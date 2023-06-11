from werkzeug.security import generate_password_hash
from sqlalchemy.sql import text
from flaskr.database import db


def get_user_by_username(username):
    sql = text('SELECT id, username, password, role FROM users WHERE username = :username')
    result = db.session.execute(sql, {"username": username})
    row = result.fetchone()
    return {'id': row[0], 'username': row[1], 'password': row[2], 'role': row[3]} if row else None


def create_user(username, password):
    hashed_password = generate_password_hash(password)
    sql = text('INSERT INTO users (username, password) VALUES (:username, :password)')
    db.session.execute(sql, {'username': username, 'password': hashed_password})
    db.session.commit()

def user_has_access_to_area(user_id, area_id):
    sql = text(
        """
        SELECT 1
        FROM areas
        LEFT JOIN secret_areas ON areas.id = secret_areas.area_id
        WHERE areas.id = :area_id
        AND (areas.is_secret = false OR secret_areas.user_id = :user_id)
        """
    )
    result = db.session.execute(sql, {"user_id": user_id, "area_id": area_id}).fetchone()
    return result is not None


def user_has_access_to_thread(user_id, thread_id):
    sql = text(
        """
        SELECT 1
        FROM threads
        JOIN areas ON threads.area_id = areas.id
        LEFT JOIN secret_areas ON areas.id = secret_areas.area_id
        WHERE threads.id = :thread_id
        AND (areas.is_secret = false OR secret_areas.user_id = :user_id)
        """
    )
    result = db.session.execute(sql, {"user_id": user_id, "thread_id": thread_id}).fetchone()
    return result is not None
