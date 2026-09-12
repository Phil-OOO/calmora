import os
import tempfile

os.environ['DATABASE_URL'] = 'sqlite:///' + os.path.join(tempfile.gettempdir(), 'calmora_test.db')

from app import create_app, db
from models import User


def test_default_admin_user_is_created():
    app = create_app('development')
    app.config['TESTING'] = True

    with app.app_context():
        db.drop_all()
        db.create_all()

        from app import create_app as fresh_create_app
        fresh_app = fresh_create_app('development')

        with fresh_app.app_context():
            user = User.query.filter_by(username='admin').first()
            assert user is not None
            assert user.check_password('Admin1234')

            client = fresh_app.test_client()
            response = client.post(
                '/auth/login',
                data={'identifier': 'admin', 'password': 'Admin1234', 'remember': 'on'},
                follow_redirects=False,
            )
            assert response.status_code == 302
            assert response.headers.get('Location') == '/'
