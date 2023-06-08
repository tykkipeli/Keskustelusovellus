from flask import Blueprint, request, redirect, url_for, session, render_template, abort
from flaskr.queries.message import delete_message, get_message, update_message
from flaskr.utils import check_csrf, validate_content

bp = Blueprint('message', __name__, url_prefix='/message')

@bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    check_csrf()
    message = get_message_or_abort(id)
    check_edit_permission(message, session.get('user_id'), session.get('role'))
    delete_message(id)
    return redirect(url_for('thread.show', id=message['thread_id']))

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    message = get_message_or_abort(id)
    check_edit_permission(message, session.get('user_id'), session.get('role'))
    error = None
    if request.method == 'POST':
        check_csrf()
        content = request.form['content']
        error = validate_content(content, 2000)
        if error is None:
            update_message(id, content)
            return redirect(url_for('thread.show', id=message['thread_id']))
    return render_template('edit_message.html', message=message, error=error)


def get_message_or_abort(id):
    message = get_message(id)
    if not message:
        abort(404)
    return message

def check_edit_permission(message, user_id, user_role):
    if user_role != 'admin' and user_id != message['sender_id']:
        abort(403)
