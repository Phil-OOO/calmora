"""
Calmora Utilities
Helper functions, Jinja2 filters, and shared logic.
"""
from datetime import datetime, date, timedelta


# ─── Jinja2 Template Filters ───────────────────────────────────────────────────

def format_date(value, fmt='%B %d, %Y'):
    """Format a date/datetime object for display."""
    if not value:
        return '—'
    if isinstance(value, datetime):
        return value.strftime(fmt)
    if isinstance(value, date):
        return value.strftime(fmt)
    return value


def format_datetime(value, fmt='%b %d, %Y at %I:%M %p'):
    """Format datetime for display."""
    if not value:
        return '—'
    if isinstance(value, datetime):
        return value.strftime(fmt)
    return value


def time_ago(dt):
    """Return human-readable time difference (e.g., '2 hours ago')."""
    if not dt:
        return '—'
    now = datetime.utcnow()
    if isinstance(dt, date) and not isinstance(dt, datetime):
        dt = datetime.combine(dt, datetime.min.time())
    diff = now - dt
    seconds = int(diff.total_seconds())
    if seconds < 60:
        return 'just now'
    elif seconds < 3600:
        m = seconds // 60
        return f'{m} minute{"s" if m > 1 else ""} ago'
    elif seconds < 86400:
        h = seconds // 3600
        return f'{h} hour{"s" if h > 1 else ""} ago'
    elif seconds < 604800:
        d = seconds // 86400
        return f'{d} day{"s" if d > 1 else ""} ago'
    else:
        return format_date(dt)


def mood_emoji(mood_type):
    """Return emoji for a mood type string."""
    emojis = {
        'happy': '😊', 'joyful': '😄', 'excited': '🤩', 'grateful': '🙏',
        'calm': '😌', 'neutral': '😐', 'tired': '😴', 'anxious': '😰',
        'sad': '😢', 'angry': '😠', 'frustrated': '😤', 'depressed': '😞',
        'hopeful': '🌟', 'confused': '😕', 'overwhelmed': '🌊', 'lonely': '💔',
        'content': '😊', 'stressed': '😫', 'irritable': '😒', 'fearful': '😨'
    }
    return emojis.get(mood_type.lower() if mood_type else '', '😐')


def mood_color(mood_score):
    """Return Bootstrap color class based on mood score 1-10."""
    if mood_score is None:
        return 'secondary'
    if mood_score >= 8:
        return 'success'
    elif mood_score >= 6:
        return 'info'
    elif mood_score >= 4:
        return 'warning'
    else:
        return 'danger'


# ─── Analytics Helpers ─────────────────────────────────────────────────────────

def get_date_range(period='week'):
    """Return (start_date, end_date) for a given period string."""
    today = date.today()
    if period == 'today':
        return today, today
    elif period == 'week':
        start = today - timedelta(days=6)
        return start, today
    elif period == 'month':
        start = today.replace(day=1)
        return start, today
    elif period == '3months':
        start = today - timedelta(days=90)
        return start, today
    elif period == 'year':
        start = today.replace(month=1, day=1)
        return start, today
    return today - timedelta(days=6), today


def calculate_streak(logs, date_field='log_date'):
    """Calculate current streak from a list of log objects."""
    if not logs:
        return 0
    sorted_logs = sorted(logs, key=lambda x: getattr(x, date_field), reverse=True)
    streak = 0
    check_date = date.today()
    for log in sorted_logs:
        log_date = getattr(log, date_field)
        if isinstance(log_date, datetime):
            log_date = log_date.date()
        if log_date == check_date:
            streak += 1
            check_date -= timedelta(days=1)
        else:
            break
    return streak


def paginate_query(query, page, per_page=10):
    """Return paginated query result."""
    return query.paginate(page=page, per_page=per_page, error_out=False)


MOOD_TYPES = [
    'happy', 'joyful', 'excited', 'grateful', 'hopeful', 'content',
    'calm', 'neutral', 'tired', 'confused',
    'anxious', 'stressed', 'overwhelmed', 'frustrated', 'irritable',
    'sad', 'depressed', 'lonely', 'angry', 'fearful'
]

SYMPTOM_CATEGORIES = ['physical', 'mental', 'emotional', 'sleep', 'appetite', 'cognitive']

HABIT_CATEGORIES = ['wellness', 'exercise', 'sleep', 'nutrition', 'social', 'mindfulness', 'learning', 'creativity']

THERAPY_TYPES = ['individual', 'group', 'couples', 'family', 'cbt', 'dbt', 'emdr', 'online']

MEDICATION_TYPES = ['prescription', 'supplement', 'otc', 'herbal', 'vitamin']