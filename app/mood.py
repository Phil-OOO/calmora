from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from models import MoodEntry

mood_bp = Blueprint('mood', __name__)


@mood_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        mood_type = request.form.get('mood_type', '').strip()
        mood_score = request.form.get('mood_score', type=int, default=5)
        notes = request.form.get('notes', '').strip()
        if not mood_type:
            flash('Please choose a mood.', 'danger')
        else:
            entry = MoodEntry(
                user_id=current_user.id,
                mood_type=mood_type,
                mood_score=mood_score,
                notes=notes,
            )
            db.session.add(entry)
            db.session.commit()
            flash('Mood entry saved.', 'success')
            return redirect(url_for('mood.index'))

    entries = MoodEntry.query.filter_by(user_id=current_user.id).order_by(MoodEntry.created_at.desc()).all()
    return render_template('mood.html', entries=entries)
