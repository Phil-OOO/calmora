from flask import Blueprint, render_template
from flask_login import current_user, login_required

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/')
@login_required
def index():
    if not getattr(current_user, 'is_admin', False):
        return render_template('access_denied.html')
    return render_template('admin.html')
