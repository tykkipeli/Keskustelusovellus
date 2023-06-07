from flask import Blueprint, render_template, request, session, redirect, url_for, abort
from flaskr.queries.message import get_messages_by_thread_id, create_message
from flaskr.queries.thread import get_thread, delete_thread, update_thread
from flaskr.queries.user import user_has_access_to_thread
from flaskr.utils import check_csrf, validate_content, validate_title

bp = Blueprint('thread', __name__, url_prefix='/thread')


@bp.route('/<int:id>', methods=('GET', 'POST'))
def show(id):
    thread = get_thread_or_abort(id)
    check_read_permission(thread, session.get('user_id'), session.get('role'))
    error = None
    if request.method == 'POST':
        check_csrf()
        content = request.form['content']
        error = validate_content(content, 2000)
        if error is None:
            create_message(content, id, session['user_id'])
            return redirect(url_for('thread.show', id=id))
    messages = get_messages_by_thread_id(id)
    return render_template('thread.html', thread=thread, messages=messages, error=error)


@bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    check_csrf()
    thread = get_thread_or_abort(id)
    check_edit_permission(thread, session.get('user_id'), session.get('role'))
    delete_thread(id)
    return redirect(url_for('area.show', id=thread['area_id']))


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    thread = get_thread_or_abort(id)
    check_edit_permission(thread, session.get('user_id'), session.get('role'))
    error = None
    if request.method == 'POST':
        check_csrf()
        title = request.form['title']
        error = validate_title(title, 100)
        if error is None:
            update_thread(id, title)
            return redirect(url_for('area.show', id=thread['area_id']))
    return render_template('edit_thread.html', thread=thread, error=error)


def get_thread_or_abort(id):
    thread = get_thread(id)
    if not thread:
        abort(404)
    return thread


def check_read_permission(thread, user_id, user_role):
    if user_role != 'admin' and not user_has_access_to_thread(user_id, thread['id']):
        abort(403)


def check_edit_permission(thread, user_id, user_role):
    if user_role != 'admin' and thread['creator_id'] != user_id:
        abort(403)
