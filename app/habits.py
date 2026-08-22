from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from models import Habit

habits_bp = Blueprint('habits', __name__)


@habits_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        category = request.form.get('category', 'wellness').strip()
        if not name:
            flash('Please enter a habit name.', 'danger')
        else:
            habit = Habit(
                user_id=current_user.id,
                name=name,
                description=description,
                category=category,
            )
            db.session.add(habit)
            db.session.commit()
            flash('Habit added.', 'success')
            return redirect(url_for('habits.index'))

    habits = Habit.query.filter_by(user_id=current_user.id).order_by(Habit.created_at.desc()).all()
    return render_template('habits.html', habits=habits)
