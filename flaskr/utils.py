from flask import request, session, abort
import re
from datetime import datetime

def check_csrf():
    if session.get('csrf_token') != request.form.get('csrf_token'):
        abort(403)

def check_admin():
    if session.get('role') != 'admin':
        abort(403)
    check_csrf()

def validate_username(username):
    if not username:
        return False, 'Username must not be empty.'
    elif not re.match('^[a-zA-Z0-9_]{3,15}$', username):
        return False, 'Username must be between 3 and 15 characters long and can only contain letters, numbers, and underscores.'
    return True, ''

def validate_password(password):
    if not password:
        return False, 'Password must not be empty.'
    elif len(password) < 8:
        return False, 'Password must be at least 8 characters long.'
    return True, ''

def validate_content(content, max_length):
    content = content.strip() 
    if not content:
        return 'Message may not be empty or consist only of whitespace.'
    elif len(content) > max_length:
        return f'Message is too long. Maximum length is {max_length} characters.'
    else:
        return None

def validate_title(title, max_length):
    title = title.strip()  
    if not title:
        return 'Title may not be empty or consist only of whitespace.'
    elif len(title) > max_length:
        return f'Title is too long. Maximum length is {max_length} characters.'
    else:
        return None

def format_timestamp(timestamp):
    try:
        timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
        return timestamp.strftime('%d.%m.%Y %H:%M:%S')
    except ValueError:
        return timestamp
    except TypeError:
        return timestamp.strftime('%d.%m.%Y %H:%M:%S')
