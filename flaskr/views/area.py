from flask import Blueprint, render_template, request, session, redirect, url_for, abort, flash
from sqlalchemy.exc import IntegrityError
from flaskr.queries.area import get_area, create_area, delete_area, delete_user_from_area, add_user_to_area, get_users_with_access
from flaskr.queries.thread import get_threads_by_area_id, create_thread
from flaskr.queries.user import get_user_by_username, user_has_access_to_area
from flaskr.utils import check_csrf, check_admin, validate_content, validate_title

bp = Blueprint('area', __name__, url_prefix='/area')

@bp.route('/<int:id>', methods=('GET', 'POST'))
def show(id):
    area = get_area_or_abort(id)
    check_read_permission(area, session.get('user_id'), session.get('role'))
    error = None
    if request.method == 'POST':
        check_csrf()
        title = request.form['title']
        initial_message = request.form['initial_message']
        error = validate_title(title, 100)
        if not error:
            error = validate_content(initial_message, 2000)
        if not error:
            create_thread(title, id, session.get('user_id'), initial_message)
            return redirect(url_for('area.show', id=id))
    threads = get_threads_by_area_id(id)
    users_with_access = []
    if area['is_secret']:
        users_with_access = get_users_with_access(id)
    return render_template('area.html', area=area, threads=threads, users=users_with_access, error=error)

@bp.route('/create', methods=['POST'])
def create():
    check_admin()
    name = request.form['name']
    is_secret = 'is_secret' in request.form
    create_area(name, is_secret)
    return redirect(url_for('home.index'))

@bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    check_admin()
    delete_area(id)
    return redirect(url_for('home.index'))

@bp.route('/deny_access/<int:area_id>/<int:user_id>', methods=['POST'])
def deny_access(area_id, user_id):
    check_admin()
    delete_user_from_area(user_id, area_id)
    return redirect(url_for('area.show', id=area_id))

@bp.route('/grant_access/<int:area_id>', methods=['POST'])
def grant_access(area_id):
    check_admin()
    username = request.form['username']
    user = get_user_by_username(username)
    if not user:
        flash('No user found with this username', 'error')
        return redirect(url_for('area.show', id=area_id))
    try:
        add_user_to_area(user['id'], area_id)
    except IntegrityError:
        flash('User already has access to this area', 'error')
    return redirect(url_for('area.show', id=area_id))


def get_area_or_abort(id):
    area = get_area(id)
    if not area:
        abort(404)
    return area

def check_read_permission(area, user_id, user_role):
    if user_role != "admin" and not user_has_access_to_area(user_id, area["id"]):
        abort(403)


