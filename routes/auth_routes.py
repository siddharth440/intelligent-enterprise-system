from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models.db_models import db, User, UserProfile
from utils.helpers import log_activity

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))
        
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        role = request.form.get('role', 'user') # 'user' or 'admin'

        if not full_name or not email or not password:
            flash('Please fill in all required fields.', 'danger')
            return render_template('auth/register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/register.html')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address is already registered.', 'warning')
            return render_template('auth/register.html')

        new_user = User(full_name=full_name, email=email, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        # Create empty profile
        profile = UserProfile(user_id=new_user.id)
        db.session.add(profile)
        db.session.commit()

        log_activity(new_user.id, 'Account Registration', f'User registered as {role}')
        flash('Registration successful! Please login to continue.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('user.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=True)
            log_activity(user.id, 'User Login', 'Successful authentication')
            flash(f'Welcome back, {user.full_name}!', 'success')
            
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
                
            if user.is_admin():
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('user.dashboard'))
        else:
            flash('Invalid email address or password.', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    log_activity(current_user.id, 'User Logout', 'User logged out')
    logout_user()
    flash('You have been logged out securely.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Password reset instructions have been sent to your email (Demo Mode: Contact admin if needed).', 'info')
        else:
            flash('No account registered with that email address.', 'warning')
        return redirect(url_for('auth.login'))
    return render_template('auth/forgot_password.html')
