from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from models import TherapySession

therapy_bp = Blueprint('therapy', __name__)


@therapy_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        therapist_name = request.form.get('therapist_name', '').strip()
        session_type = request.form.get('session_type', 'individual').strip() or 'individual'
        scheduled_at = request.form.get('scheduled_at', '').strip()
        duration_minutes = request.form.get('duration_minutes', type=int, default=60)
        location = request.form.get('location', '').strip()
        status = request.form.get('status', 'scheduled').strip() or 'scheduled'
        notes = request.form.get('notes', '').strip()

        if not therapist_name or not scheduled_at:
            flash('Please provide a therapist name and appointment time.', 'danger')
        else:
            try:
                scheduled_dt = datetime.fromisoformat(scheduled_at)
            except ValueError:
                flash('Please use a valid date and time for the session.', 'danger')
                return render_template('therapy.html', sessions=TherapySession.query.filter_by(user_id=current_user.id).order_by(TherapySession.scheduled_at.desc()).all())

            session = TherapySession(
                user_id=current_user.id,
                therapist_name=therapist_name,
                session_type=session_type,
                scheduled_at=scheduled_dt,
                duration_minutes=duration_minutes,
                location=location or 'Not specified',
                status=status,
                session_notes=notes,
            )
            db.session.add(session)
            db.session.commit()
            flash('Therapy session saved.', 'success')
            return redirect(url_for('therapy.index'))

    sessions = TherapySession.query.filter_by(user_id=current_user.id).order_by(TherapySession.scheduled_at.desc()).all()
    return render_template('therapy.html', sessions=sessions)
