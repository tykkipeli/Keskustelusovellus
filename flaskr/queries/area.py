from flaskr.database import db
from sqlalchemy.sql import text
from flaskr.utils import format_timestamp

def create_area(name, is_secret):
    sql = text('INSERT INTO areas (name, is_secret) VALUES (:name, :is_secret)')
    db.session.execute(sql, {'name': name, 'is_secret': is_secret})
    db.session.commit()

def get_area(id):
    sql = text('SELECT id, name, is_secret FROM areas WHERE id=:id')
    result = db.session.execute(sql, {'id': id})
    row = result.fetchone()
    return {'id': row[0], 'name': row[1], 'is_secret': row[2]} if row else None

def get_area_by_name(name):
    sql = text('SELECT id, name, is_secret FROM areas WHERE name=:name')
    result = db.session.execute(sql, {'name': name})
    row = result.fetchone()
    return {'id': row[0], 'name': row[1], 'is_secret': row[2]} if row else None

def delete_area(id):
    sql_messages = text('DELETE FROM messages WHERE thread_id IN (SELECT id FROM threads WHERE area_id = :id)')
    db.session.execute(sql_messages, {'id': id})
    sql_threads = text('DELETE FROM threads WHERE area_id = :id')
    db.session.execute(sql_threads, {'id': id})
    sql_secret_areas = text('DELETE FROM secret_areas WHERE area_id = :id')
    db.session.execute(sql_secret_areas, {'id': id})
    sql_areas = text('DELETE FROM areas WHERE id = :id')
    db.session.execute(sql_areas, {'id': id})
    db.session.commit()

def get_areas(user_id, role):
    base_sql = """
        SELECT areas.id, areas.name, areas.is_secret, 
        COUNT(DISTINCT threads.id) AS num_threads,
        COUNT(messages.id) AS num_messages, 
        COALESCE(MAX(messages.timestamp)::text, '-') AS latest_message_timestamp
        FROM areas 
        LEFT JOIN threads ON areas.id = threads.area_id
        LEFT JOIN messages ON threads.id = messages.thread_id
    """
    if role == 'admin':
        sql = text(base_sql + """
            GROUP BY areas.id
            ORDER BY areas.id
        """)
        result = db.session.execute(sql)
    else:
        sql = text(base_sql + """
            LEFT JOIN secret_areas ON areas.id = secret_areas.area_id 
            WHERE areas.is_secret = false OR secret_areas.user_id = :user_id
            GROUP BY areas.id
            ORDER BY areas.id
        """)
        result = db.session.execute(sql, {'user_id': user_id})

    return [{'id': row[0], 'name': row[1], 'is_secret': row[2], 
             'num_threads': row[3], 'num_messages': row[4], 
             'latest_message_timestamp': format_timestamp(row[5])} for row in result.fetchall()]

def add_user_to_area(user_id, area_id):
    sql = text('INSERT INTO secret_areas (user_id, area_id) VALUES (:user_id, :area_id)')
    db.session.execute(sql, {'user_id': user_id, 'area_id': area_id})
    db.session.commit()

def delete_user_from_area(user_id, area_id):
    sql = text('DELETE FROM secret_areas WHERE user_id = :user_id AND area_id = :area_id')
    db.session.execute(sql, {'user_id': user_id, 'area_id': area_id})
    db.session.commit()

def get_users_with_access(area_id):
    sql = text(
        """
        SELECT users.id, users.username
        FROM users
        JOIN secret_areas ON users.id = secret_areas.user_id
        WHERE secret_areas.area_id = :area_id
        """
    )
    result = db.session.execute(sql, {'area_id': area_id})
    return [{'id': row[0], 'username': row[1]} for row in result.fetchall()]
