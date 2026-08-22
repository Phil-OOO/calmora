from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

search_bp = Blueprint('search', __name__)


@search_bp.route('/')
@login_required
def index():
    query = request.args.get('q', '').strip()
    return render_template('search.html', query=query, results=[])
