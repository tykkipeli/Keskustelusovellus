from sqlalchemy.sql import text
from flaskr.database import db

def create_thread(title, area_id, creator_id, initial_message):
    sql = text('INSERT INTO threads (title, area_id, creator_id) VALUES (:title, :area_id, :creator_id) RETURNING id')
    result = db.session.execute(sql, {'title': title, 'area_id': area_id, 'creator_id': creator_id})
    thread_id = result.fetchone()[0]

    sql_msg = text('INSERT INTO messages (content, thread_id, sender_id) VALUES (:content, :thread_id, :sender_id)')
    db.session.execute(sql_msg, {'content': initial_message, 'thread_id': thread_id, 'sender_id': creator_id})

    db.session.commit()

def get_thread(id):
    sql = text('SELECT id, title, creator_id, area_id FROM threads WHERE id=:id')
    result = db.session.execute(sql, {'id': id})
    row = result.fetchone()
    return {'id': row[0], 'title': row[1], 'creator_id': row[2], 'area_id': row[3]} if row else None

def update_thread(id, title):
    sql = text('UPDATE threads SET title = :title WHERE id = :id')
    db.session.execute(sql, {'id': id, 'title': title})
    db.session.commit()

def delete_thread(id):
    sql_messages = text('DELETE FROM messages WHERE thread_id = :id')
    db.session.execute(sql_messages, {'id': id})
    sql_thread = text('DELETE FROM threads WHERE id = :id')
    db.session.execute(sql_thread, {'id': id})
    db.session.commit()

def get_threads_by_area_id(area_id):
    sql = text('SELECT id, title, creator_id FROM threads WHERE area_id=:area_id')
    result = db.session.execute(sql, {'area_id': area_id})
    return [{'id': row[0], 'title': row[1], 'creator_id': row[2]} for row in result]
