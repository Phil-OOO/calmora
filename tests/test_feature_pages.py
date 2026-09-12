from app import create_app, db
from models import JournalEntry, MoodEntry, TherapySession, User


def test_therapy_and_search_features_work():
    app = create_app('development')
    app.config['TESTING'] = True
    with app.app_context():
        db.drop_all()
        db.create_all()

        admin = User(
            username='admin',
            email='admin@calmora.local',
            full_name='Calmora Admin',
            is_admin=True,
            is_active=True,
        )
        admin.set_password('Admin1234')
        db.session.add(admin)
        db.session.commit()

        mood = MoodEntry(user_id=admin.id, mood_type='happy', mood_score=8, notes='Feeling better')
        journal = JournalEntry(user_id=admin.id, title='Calm morning', content='A calm morning helped me focus.', mood_score=8)
        db.session.add_all([mood, journal])
        db.session.commit()

        client = app.test_client()
        client.post('/auth/login', data={'identifier': 'admin', 'password': 'Admin1234'}, follow_redirects=False)

        analytics_response = client.get('/analytics/')
        assert analytics_response.status_code == 200

        therapy_response = client.post(
            '/therapy/',
            data={
                'therapist_name': 'Dr. Wells',
                'session_type': 'individual',
                'scheduled_at': '2026-09-20T10:00',
                'duration_minutes': '60',
                'location': 'Online',
                'status': 'scheduled',
                'notes': 'Focus on calm routines',
            },
            follow_redirects=False,
        )
        assert therapy_response.status_code == 302
        assert TherapySession.query.filter_by(user_id=admin.id).count() == 1

        search_response = client.get('/search/?q=calm')
        assert search_response.status_code == 200
        body = search_response.get_data(as_text=True).lower()
        assert 'calm morning' in body or 'calm' in body


def test_user_registration_creates_account():
    app = create_app('development')
    app.config['TESTING'] = True

    with app.app_context():
        db.drop_all()
        db.create_all()

        client = app.test_client()
        response = client.post(
            '/auth/register',
            data={
                'full_name': 'New User',
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password': 'Password123',
                'confirm_password': 'Password123',
            },
            follow_redirects=False,
        )

        assert response.status_code == 302
        assert response.headers.get('Location') == '/'
        user = User.query.filter_by(username='newuser').first()
        assert user is not None
        assert user.email == 'newuser@example.com'
        assert user.check_password('Password123')
