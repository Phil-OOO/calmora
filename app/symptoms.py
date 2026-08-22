from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from models import SymptomEntry

symptoms_bp = Blueprint('symptoms', __name__)


@symptoms_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        symptom_name = request.form.get('symptom_name', '').strip()
        severity = request.form.get('severity', type=int, default=5)
        notes = request.form.get('notes', '').strip()
        if not symptom_name:
            flash('Please enter a symptom name.', 'danger')
        else:
            entry = SymptomEntry(
                user_id=current_user.id,
                symptom_name=symptom_name,
                severity=severity,
                notes=notes,
            )
            db.session.add(entry)
            db.session.commit()
            flash('Symptom logged.', 'success')
            return redirect(url_for('symptoms.index'))

    symptoms = SymptomEntry.query.filter_by(user_id=current_user.id).order_by(SymptomEntry.created_at.desc()).all()
    return render_template('symptoms.html', symptoms=symptoms)
