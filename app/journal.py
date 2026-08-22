from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from models import JournalEntry

journal_bp = Blueprint('journal', __name__)


@journal_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        mood_score = request.form.get('mood_score', type=int, default=5)
        tags = request.form.get('tags', '').strip()
        if not title or not content:
            flash('Please add both a title and some journal content.', 'danger')
        else:
            entry = JournalEntry(
                user_id=current_user.id,
                title=title,
                content=content,
                mood_score=mood_score,
                tags=tags,
                word_count=len(content.split()),
            )
            db.session.add(entry)
            db.session.commit()
            flash('Journal entry saved.', 'success')
            return redirect(url_for('journal.index'))

    entries = JournalEntry.query.filter_by(user_id=current_user.id).order_by(JournalEntry.created_at.desc()).all()
    return render_template('journal.html', entries=entries)