from flask import Blueprint, render_template
from flask_login import current_user, login_required

from models import Habit, JournalEntry, MoodEntry, SymptomEntry, TherapySession

analytics_bp = Blueprint('analytics', __name__)


@analytics_bp.route('/')
@login_required
def index():
    moods = MoodEntry.query.filter_by(user_id=current_user.id).all()
    journals = JournalEntry.query.filter_by(user_id=current_user.id).all()
    symptoms = SymptomEntry.query.filter_by(user_id=current_user.id).all()
    therapy_sessions = TherapySession.query.filter_by(user_id=current_user.id).all()
    habits = Habit.query.filter_by(user_id=current_user.id).all()

    avg_mood = round(sum(entry.mood_score for entry in moods) / len(moods), 1) if moods else 0
    journal_count = len(journals)
    symptom_count = len(symptoms)
    therapy_count = len(therapy_sessions)
    habit_count = len(habits)

    stats = {
        'avg_mood': avg_mood,
        'journal_count': journal_count,
        'symptom_count': symptom_count,
        'therapy_count': therapy_count,
        'habit_count': habit_count,
    }

    chart_data = {
        'labels': ['Mood', 'Journal', 'Symptoms', 'Therapy', 'Habits'],
        'values': [max(avg_mood * 10, 0), journal_count * 10, symptom_count * 10, therapy_count * 10, habit_count * 10],
    }
    chart_items = list(zip(chart_data['labels'], chart_data['values']))

    return render_template('analytics.html', stats=stats, chart_data=chart_data, chart_items=chart_items)
