from flask import Blueprint, render_template, request, session
from flaskr.queries.message import search_messages
from flaskr.queries.area import get_areas

bp = Blueprint('home', __name__)

@bp.route('/', methods=['GET'])
def index():
    user_id = session.get('user_id')
    role = session.get('role')
    return render_template('home.html', areas=get_areas(user_id, role))

@bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    user_id = session.get('user_id')
    role = session.get('role')
    messages = search_messages(query, user_id, role)
    return render_template('search_results.html', messages=messages)