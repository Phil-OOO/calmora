"""
Auth Routes - Login, Register, Logout, Profile Management
"""
from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from app import db
from app.models import User
from app.auth import auth


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        identifier = request.form.get('identifier', '').strip()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember'))
        
        # Allow login with email or username
        user = User.query.filter(
            (User.email == identifier) | (User.username == identifier)
        ).first()
        
        if user and user.check_password(password) and user.is_active:
            login_user(user, remember=remember)
            user.last_login = datetime.utcnow()
            db.session.commit()
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.full_name.split()[0]}! 🌿', 'success')
            return redirect(next_page or url_for('dashboard.index'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    
    return render_template('auth/login.html', title='Sign In')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        username = request.form.get('username', '').strip().lower()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        
        # Validation
        errors = []
        if not full_name or len(full_name) < 2:
            errors.append('Please enter your full name.')
        if not username or len(username) < 3:
            errors.append('Username must be at least 3 characters.')
        if User.query.filter_by(username=username).first():
            errors.append('That username is already taken.')
        if User.query.filter_by(email=email).first():
            errors.append('An account with that email already exists.')
        if len(password) < 8:
            errors.append('Password must be at least 8 characters.')
        if password != confirm:
            errors.append('Passwords do not match.')
        
        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('auth/register.html', title='Create Account',
                                   form_data=request.form)
        
        user = User(full_name=full_name, username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        flash(f'Welcome to Calmora, {full_name.split()[0]}! Your journey begins here. 🌱', 'success')
        return redirect(url_for('dashboard.index'))
    
    return render_template('auth/register.html', title='Create Account')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You\'ve been signed out. Take care! 💙', 'info')
    return redirect(url_for('auth.login'))


@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'update_profile':
            current_user.full_name = request.form.get('full_name', '').strip()
            current_user.bio = request.form.get('bio', '').strip()
            current_user.timezone = request.form.get('timezone', 'UTC')
            db.session.commit()
            flash('Profile updated successfully.', 'success')
        
        elif action == 'change_password':
            current_pw = request.form.get('current_password', '')
            new_pw = request.form.get('new_password', '')
            confirm_pw = request.form.get('confirm_password', '')
            
            if not current_user.check_password(current_pw):
                flash('Current password is incorrect.', 'danger')
            elif len(new_pw) < 8:
                flash('New password must be at least 8 characters.', 'danger')
            elif new_pw != confirm_pw:
                flash('New passwords do not match.', 'danger')
            else:
                current_user.set_password(new_pw)
                db.session.commit()
                flash('Password changed successfully.', 'success')
        
        elif action == 'toggle_theme':
            current_user.theme = 'dark' if current_user.theme == 'light' else 'light'
            db.session.commit()
            return {'theme': current_user.theme}, 200
        
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/profile.html', title='My Profile')