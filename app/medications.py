from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from models import Medication

medications_bp = Blueprint('medications', __name__)


@medications_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        dosage = request.form.get('dosage', '').strip()
        frequency = request.form.get('frequency', '').strip()
        start_date = request.form.get('start_date')
        if not name or not dosage or not frequency or not start_date:
            flash('Please fill in the medication name, dosage, frequency, and start date.', 'danger')
        else:
            medication = Medication(
                user_id=current_user.id,
                name=name,
                dosage=dosage,
                frequency=frequency,
                start_date=start_date,
            )
            db.session.add(medication)
            db.session.commit()
            flash('Medication added.', 'success')
            return redirect(url_for('medications.index'))

    medications = Medication.query.filter_by(user_id=current_user.id).order_by(Medication.created_at.desc()).all()
    return render_template('medications.html', medications=medications)
