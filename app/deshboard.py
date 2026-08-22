from flask import Blueprint, render_template
from flask_login import login_required, current_user

from models import JournalEntry, MoodEntry


dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@login_required
def index():
    mood_entries = MoodEntry.query.filter_by(user_id=current_user.id).order_by(MoodEntry.created_at.desc()).limit(5).all()
    journal_entries = JournalEntry.query.filter_by(user_id=current_user.id).order_by(JournalEntry.created_at.desc()).limit(5).all()

    return render_template(
        'dashboard.html',
        user=current_user,
        mood_entries=mood_entries,
        journal_entries=journal_entries,
        mood_count=len(mood_entries),
        journal_count=len(journal_entries),
    )