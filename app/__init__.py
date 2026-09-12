import os
import sys

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from config import config


# Initialize extensions
app_db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
migrate = Migrate()


@login_manager.user_loader
def load_user(user_id):
    from models import User

    return app_db.session.get(User, int(user_id))


def create_app(config_name='default'):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config[config_name])

    app_db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, app_db)

    app.config['WTF_CSRF_ENABLED'] = False

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please sign in to access Calmora.'
    login_manager.login_message_category = 'info'

    from app.auth import auth_bp
    from app.deshboard import dashboard_bp
    from app.journal import journal_bp
    from app.mood import mood_bp
    from app.symptoms import symptoms_bp
    from app.medications import medications_bp
    from app.therapy import therapy_bp
    from app.habits import habits_bp
    from app.analytics import analytics_bp
    from app.admin import admin_bp
    from app.search import search_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/')
    app.register_blueprint(journal_bp, url_prefix='/journal')
    app.register_blueprint(mood_bp, url_prefix='/mood')
    app.register_blueprint(symptoms_bp, url_prefix='/symptoms')
    app.register_blueprint(medications_bp, url_prefix='/medications')
    app.register_blueprint(therapy_bp, url_prefix='/therapy')
    app.register_blueprint(habits_bp, url_prefix='/habits')
    app.register_blueprint(analytics_bp, url_prefix='/analytics')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(search_bp, url_prefix='/search')

    with app.app_context():
        import models  # noqa: F401
        app_db.create_all()

        from models import User
        if User.query.filter((User.username == 'admin') | (User.email == 'admin@calmora.local')).first() is None:
            admin = User(
                username='admin',
                email='admin@calmora.local',
                full_name='Calmora Admin',
                is_admin=True,
                is_active=True,
            )
            admin.set_password('Admin1234')
            app_db.session.add(admin)
            app_db.session.commit()

    return app


db = app_db
