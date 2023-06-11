import secrets
from werkzeug.security import check_password_hash
from flask import Blueprint, render_template, request, session, redirect, url_for
from flaskr.queries.user import get_user_by_username, create_user
from flaskr.utils import validate_password, validate_username

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_valid_username, username_error = validate_username(username)
        is_valid_password, password_error = validate_password(password)
        if not is_valid_username:
            error = username_error
        elif not is_valid_password:
            error = password_error
        else:
            user = get_user_by_username(username)
            if user is None:
                create_user(username, password)
                return redirect(url_for('auth.login'))
            error = 'User already exists!'
    return render_template('register.html', error=error)

@bp.route('/login', methods=('GET', 'POST'))
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)
        if user is None:
            error = 'No such user!'
        else:
            if check_password_hash(user['password'], password):
                create_user_session(user)
                return redirect(url_for('home.index'))
            error = 'Incorrect password!'
    return render_template('login.html', error=error)

def create_user_session(user):
    session.clear()
    session['username'] = user['username']
    session['user_id'] = user['id']
    session['role'] = user['role']
    session['csrf_token'] = secrets.token_hex(16)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home.index'))
