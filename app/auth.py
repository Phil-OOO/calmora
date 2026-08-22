from datetime import datetime
import re

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from app import db
from models import User


auth_bp = Blueprint('auth', __name__)


def validate_email(email):
    return re.match(r'^[^@]+@[^@]+\.[^@]+$', email) is not None


def validate_password(password):
    return len(password) >= 8 and any(c.isalpha() for c in password) and any(c.isdigit() for c in password)


@auth_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        identifier = request.form.get('identifier', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember') == 'on'

        if not identifier or not password:
            flash('Please fill in all fields.', 'danger')
            return render_template('login.html')

        user = User.query.filter((User.email == identifier) | (User.username == identifier)).first()
        if user and user.check_password(password) and user.is_active:
            login_user(user, remember=remember)
            user.last_login = datetime.utcnow()
            db.session.commit()
            flash(f'Welcome back, {user.full_name.split()[0] if user.full_name else user.username}! 🌟', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard.index'))

        flash('Invalid username/email or password.', 'danger')

    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip().lower()
        email = request.form.get('email', '').strip().lower()
        full_name = request.form.get('full_name', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        errors = []
        if not username or len(username) < 3:
            errors.append('Username must be at least 3 characters.')
        if not re.match(r'^[a-z0-9_]+$', username):
            errors.append('Username can only contain letters, numbers, and underscores.')
        if not validate_email(email):
            errors.append('Please enter a valid email address.')
        if not validate_password(password):
            errors.append('Password must be at least 8 characters with letters and numbers.')
        if password != confirm:
            errors.append('Passwords do not match.')
        if User.query.filter((User.username == username) | (User.email == email)).first():
            errors.append('Username or email already taken.')

        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('register.html', username=username, email=email, full_name=full_name)

        user = User(username=username, email=email, full_name=full_name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash(f'Welcome to Calmora, {full_name or username}! 🎉', 'success')
        return redirect(url_for('dashboard.index'))

    return render_template('register.html')


@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out. Take care! 💙', 'info')
    return redirect(url_for('auth.login'))