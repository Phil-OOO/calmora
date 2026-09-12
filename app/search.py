from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

from models import Habit, JournalEntry, Medication, MoodEntry, SymptomEntry

search_bp = Blueprint('search', __name__)


def _matches_query(model, fields, query):
    query = query.lower()
    for field in fields:
        value = getattr(model, field, '')
        if value is None:
            continue
        if isinstance(value, str) and query in value.lower():
            return True
    return False


@search_bp.route('/')
@login_required
def index():
    query = request.args.get('q', '').strip()
    results = []

    if query:
        searches = [
            ('Journal', JournalEntry.query.filter_by(user_id=current_user.id).all(), ['title', 'content', 'tags']),
            ('Mood', MoodEntry.query.filter_by(user_id=current_user.id).all(), ['mood_type', 'notes']),
            ('Symptoms', SymptomEntry.query.filter_by(user_id=current_user.id).all(), ['symptom_name', 'notes']),
            ('Medication', Medication.query.filter_by(user_id=current_user.id).all(), ['name', 'purpose', 'notes']),
            ('Habit', Habit.query.filter_by(user_id=current_user.id).all(), ['name', 'description', 'category']),
        ]

        for section_name, items, fields in searches:
            for item in items:
                if _matches_query(item, fields, query):
                    summary = getattr(item, 'title', None) or getattr(item, 'name', None) or getattr(item, 'mood_type', None) or getattr(item, 'symptom_name', None) or getattr(item, 'medication_name', None) or 'Entry'
                    if hasattr(item, 'content') and item.content:
                        snippet = item.content[:80]
                    elif hasattr(item, 'notes') and item.notes:
                        snippet = item.notes[:80]
                    elif hasattr(item, 'description') and item.description:
                        snippet = item.description[:80]
                    else:
                        snippet = 'Matched wellness record.'
                    results.append({
                        'type': section_name,
                        'title': summary,
                        'summary': snippet,
                        'url': {
                            'Journal': '/journal/',
                            'Mood': '/mood/',
                            'Symptoms': '/symptoms/',
                            'Medication': '/medications/',
                            'Habit': '/habits/',
                        }.get(section_name, '/'),
                    })

    return render_template('search.html', query=query, results=results)
