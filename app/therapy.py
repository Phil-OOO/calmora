from flask import Blueprint, render_template
from flask_login import current_user, login_required

therapy_bp = Blueprint('therapy', __name__)


@therapy_bp.route('/')
@login_required
def index():
    return render_template('therapy.html', sessions=[])
