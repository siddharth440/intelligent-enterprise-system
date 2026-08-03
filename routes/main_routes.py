from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.db_models import db, Feedback
from flask_login import current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/about')
def about():
    return render_template('index.html', scroll_to='about')

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        message = request.form.get('message')
        rating = request.form.get('rating', 5)
        if current_user.is_authenticated and message:
            fb = Feedback(user_id=current_user.id, rating=int(rating), message=message)
            db.session.add(fb)
            db.session.commit()
            flash('Thank you! Your feedback/inquiry has been submitted successfully.', 'success')
        else:
            flash('Thank you for contacting us. We will get back to you shortly.', 'success')
        return redirect(url_for('main.index'))
    return render_template('index.html', scroll_to='contact')
