from sqlalchemy.sql import text
from flaskr.database import db
from flaskr.utils import format_timestamp

def create_message(content, thread_id, sender_id):
    sql = text('INSERT INTO messages (content, thread_id, sender_id) VALUES (:content, :thread_id, :sender_id)')
    db.session.execute(sql, {'content': content, 'thread_id': thread_id, 'sender_id': sender_id})
    db.session.commit()

def get_message(id):
    sql = text('SELECT id, content, timestamp, thread_id, sender_id FROM messages WHERE id = :id')
    result = db.session.execute(sql, {'id': id})
    row = result.fetchone()
    return {'id': row[0], 'content': row[1], 'timestamp': row[2],
            'thread_id': row[3], 'sender_id': row[4]} if row else None

def update_message(id, content):
    sql = text('UPDATE messages SET content = :content WHERE id = :id')
    db.session.execute(sql, {'id': id, 'content': content})
    db.session.commit()

def delete_message(id):
    sql = text('DELETE FROM messages WHERE id = :id')
    db.session.execute(sql, {'id': id})
    db.session.commit()

def get_messages_by_thread_id(thread_id):
    sql = text("""
        SELECT messages.id, users.username, users.id, messages.timestamp, messages.content
        FROM messages
        JOIN users ON messages.sender_id = users.id
        WHERE messages.thread_id = :thread_id 
        ORDER BY messages.timestamp
    """)
    result = db.session.execute(sql, {'thread_id': thread_id})
    messages = [{'id': row[0], 'sender': row[1], 'sender_id': row[2],
                 'timestamp': format_timestamp(row[3]), 'content': row[4]} for row in result]
    return messages

def search_messages(query, user_id, role):
    base_sql = """
        SELECT messages.content, threads.title, areas.name, threads.id, areas.id, users.username
        FROM messages
        JOIN users ON users.id = messages.sender_id
        JOIN threads ON messages.thread_id = threads.id
        JOIN areas ON threads.area_id = areas.id
    """

    if not user_id:  # if the user is not logged in
        sql = text(base_sql + """
            WHERE areas.is_secret = false AND messages.content ILIKE :query
        """)
        result = db.session.execute(sql, {'query': '%' + query + '%'})
    elif role == 'admin':  # if the user is an admin
        sql = text(base_sql + """
            WHERE messages.content ILIKE :query
        """)
        result = db.session.execute(sql, {'query': '%' + query + '%'})
    else:  # if the user is logged in and not an admin
        sql = text(base_sql + """
            LEFT JOIN secret_areas ON areas.id = secret_areas.area_id 
            WHERE (areas.is_secret = false OR secret_areas.user_id = :user_id) AND messages.content ILIKE :query
        """)
        result = db.session.execute(sql, {'user_id': user_id, 'query': '%' + query + '%'})

    messages = [{'content': row[0], 'thread': row[1], 'area': row[2],
                 'thread_id': row[3], 'area_id': row[4], 'sender': row[5]} for row in result]
    return messages
