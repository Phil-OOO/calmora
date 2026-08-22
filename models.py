"""
Calmora Database Models
All SQLAlchemy ORM models for the mental health app.
Each model represents a database table with relationships.
"""
from datetime import datetime, date
from app import db, login_manager
import bcrypt


# ─── User Model ────────────────────────────────────────────────────────────────

class User(db.Model):
    """Core user model with authentication support."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    full_name = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    avatar_url = db.Column(db.String(256), default=None)
    bio = db.Column(db.Text, default=None)
    timezone = db.Column(db.String(50), default='UTC')
    theme = db.Column(db.String(10), default='light')  # 'light' or 'dark'
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=None)

    # Relationships – one user has many entries in each module
    moods = db.relationship('MoodEntry', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    journals = db.relationship('JournalEntry', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    symptoms = db.relationship('SymptomEntry', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    medications = db.relationship('Medication', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    therapy_sessions = db.relationship('TherapySession', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    habits = db.relationship('Habit', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    # Flask-Login required properties
    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def set_password(self, password):
        """Hash and store password using bcrypt."""
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password):
        """Verify password against stored hash."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def __repr__(self):
        return f'<User {self.username}>'


@login_manager.user_loader
def load_user(user_id):
    """Flask-Login callback to load user by ID from session."""
    return User.query.get(int(user_id))


# ─── Mood Tracking ─────────────────────────────────────────────────────────────

class MoodEntry(db.Model):
    """Track emotional states with scores and context."""
    __tablename__ = 'mood_entries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mood_type = db.Column(db.String(30), nullable=False)   # e.g., 'happy','anxious'
    mood_score = db.Column(db.Integer, nullable=False)      # 1-10 scale
    energy_level = db.Column(db.Integer, default=5)         # 1-10
    stress_level = db.Column(db.Integer, default=5)         # 1-10
    sleep_hours = db.Column(db.Float, default=7.0)
    notes = db.Column(db.Text, default=None)
    triggers = db.Column(db.String(256), default=None)      # comma-separated
    activities = db.Column(db.String(256), default=None)    # comma-separated
    weather = db.Column(db.String(30), default=None)
    logged_at = db.Column(db.DateTime, default=datetime.utcnow)
    entry_date = db.Column(db.Date, default=date.today)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<MoodEntry {self.mood_type} ({self.mood_score}) on {self.entry_date}>'


# ─── Journal ───────────────────────────────────────────────────────────────────

class JournalEntry(db.Model):
    """Rich text journaling with tagging and mood correlation."""
    __tablename__ = 'journal_entries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    mood_score = db.Column(db.Integer, default=5)
    tags = db.Column(db.String(500), default=None)          # comma-separated
    is_private = db.Column(db.Boolean, default=True)
    is_favorite = db.Column(db.Boolean, default=False)
    word_count = db.Column(db.Integer, default=0)
    entry_date = db.Column(db.Date, default=date.today)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<JournalEntry "{self.title}">'


# ─── Symptom Tracking ──────────────────────────────────────────────────────────

class SymptomEntry(db.Model):
    """Track physical and mental symptoms with severity scores."""
    __tablename__ = 'symptom_entries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    symptom_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), default='general')  # physical/mental/emotional
    severity = db.Column(db.Integer, nullable=False)         # 1-10
    duration_minutes = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text, default=None)
    triggers = db.Column(db.String(256), default=None)
    relievers = db.Column(db.String(256), default=None)
    entry_date = db.Column(db.Date, default=date.today)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<SymptomEntry {self.symptom_name} ({self.severity})>'


# ─── Medication Management ─────────────────────────────────────────────────────

class Medication(db.Model):
    """Manage prescriptions with dosing schedules."""
    __tablename__ = 'medications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(50), nullable=False)        # e.g., '50mg'
    frequency = db.Column(db.String(50), nullable=False)     # e.g., 'twice daily'
    medication_type = db.Column(db.String(50), default='prescription')
    prescriber = db.Column(db.String(100), default=None)
    purpose = db.Column(db.String(200), default=None)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, default=None)
    refill_date = db.Column(db.Date, default=None)
    notes = db.Column(db.Text, default=None)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Each medication has many dose logs
    dose_logs = db.relationship('MedicationLog', backref='medication',
                                 lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Medication {self.name} {self.dosage}>'


class MedicationLog(db.Model):
    """Track individual medication doses taken."""
    __tablename__ = 'medication_logs'

    id = db.Column(db.Integer, primary_key=True)
    medication_id = db.Column(db.Integer, db.ForeignKey('medications.id'), nullable=False)
    taken_at = db.Column(db.DateTime, default=datetime.utcnow)
    scheduled_time = db.Column(db.String(10), default=None)  # 'HH:MM'
    was_taken = db.Column(db.Boolean, default=True)
    notes = db.Column(db.String(200), default=None)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<MedicationLog {self.medication_id} taken={self.was_taken}>'


# ─── Therapy Sessions ──────────────────────────────────────────────────────────

class TherapySession(db.Model):
    """Schedule and log therapy appointments."""
    __tablename__ = 'therapy_sessions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    therapist_name = db.Column(db.String(100), nullable=False)
    session_type = db.Column(db.String(50), default='individual')  # individual/group/online
    scheduled_at = db.Column(db.DateTime, nullable=False)
    duration_minutes = db.Column(db.Integer, default=60)
    location = db.Column(db.String(200), default=None)
    status = db.Column(db.String(20), default='scheduled')   # scheduled/completed/cancelled
    mood_before = db.Column(db.Integer, default=None)
    mood_after = db.Column(db.Integer, default=None)
    session_notes = db.Column(db.Text, default=None)
    homework = db.Column(db.Text, default=None)
    cost = db.Column(db.Float, default=None)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<TherapySession with {self.therapist_name} at {self.scheduled_at}>'


# ─── Habit Tracking ────────────────────────────────────────────────────────────

class Habit(db.Model):
    """Define habits to build or break."""
    __tablename__ = 'habits'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, default=None)
    category = db.Column(db.String(50), default='wellness')   # wellness/sleep/exercise/social
    habit_type = db.Column(db.String(10), default='build')    # 'build' or 'break'
    frequency = db.Column(db.String(20), default='daily')     # daily/weekly
    target_count = db.Column(db.Integer, default=1)           # times per frequency period
    color = db.Column(db.String(7), default='#6366f1')        # hex color for UI
    icon = db.Column(db.String(50), default='⭐')
    is_active = db.Column(db.Boolean, default=True)
    start_date = db.Column(db.Date, default=date.today)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Each habit has many completion logs
    logs = db.relationship('HabitLog', backref='habit', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def current_streak(self):
        """Calculate current consecutive completion streak."""
        from datetime import timedelta
        logs = self.logs.filter_by(completed=True).order_by(HabitLog.log_date.desc()).all()
        if not logs:
            return 0
        streak = 0
        check_date = date.today()
        for log in logs:
            if log.log_date == check_date:
                streak += 1
                check_date -= timedelta(days=1)
            else:
                break
        return streak

    def __repr__(self):
        return f'<Habit {self.name}>'


class HabitLog(db.Model):
    """Daily habit completion records."""
    __tablename__ = 'habit_logs'

    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False)
    log_date = db.Column(db.Date, default=date.today)
    completed = db.Column(db.Boolean, default=False)
    count = db.Column(db.Integer, default=1)
    notes = db.Column(db.String(200), default=None)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<HabitLog {self.habit_id} on {self.log_date}>'