import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models.db_models import db, UserProfile, Skill, Prediction, Recommendation, ActivityLog
from config import Config
from utils.resume_parser import parse_pdf_resume
from utils.chatbot_engine import generate_chat_response
from utils.helpers import log_activity

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/dashboard')
@login_required
def dashboard():
    profile = UserProfile.query.filter_by(user_id=current_user.id).first()
    latest_prediction = Prediction.query.filter_by(user_id=current_user.id).order_by(Prediction.created_at.desc()).first()
    recommendations = Recommendation.query.filter_by(user_id=current_user.id).order_by(Recommendation.created_at.desc()).all()
    skills = Skill.query.filter_by(user_id=current_user.id).all()
    activities = ActivityLog.query.filter_by(user_id=current_user.id).order_by(ActivityLog.timestamp.desc()).limit(5).all()

    return render_template('user/dashboard.html', 
                           profile=profile, 
                           prediction=latest_prediction, 
                           recommendations=recommendations, 
                           skills=skills,
                           activities=activities)


@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_prof = UserProfile.query.filter_by(user_id=current_user.id).first()
    if not user_prof:
        user_prof = UserProfile(user_id=current_user.id)
        db.session.add(user_prof)
        db.session.commit()

    if request.method == 'POST':
        user_prof.phone = request.form.get('phone')
        user_prof.age = int(request.form.get('age')) if request.form.get('age') else None
        user_prof.gender = request.form.get('gender')
        user_prof.education = request.form.get('education')
        user_prof.college = request.form.get('college')
        user_prof.department = request.form.get('department')
        user_prof.programming_languages = request.form.get('programming_languages')
        user_prof.experience_years = int(request.form.get('experience_years', 0))
        user_prof.projects_count = int(request.form.get('projects_count', 0))
        user_prof.interests = request.form.get('interests')

        # Handle skill inputs
        skills_raw = request.form.get('skills_input', '')
        if skills_raw:
            # Clear old skills and insert new
            Skill.query.filter_by(user_id=current_user.id).delete()
            for s in skills_raw.split(','):
                s_clean = s.strip()
                if s_clean:
                    db.session.add(Skill(user_id=current_user.id, skill_name=s_clean, proficiency='Intermediate'))

        db.session.commit()
        log_activity(current_user.id, 'Profile Update', 'Updated profile information and skill matrix')
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('user.profile'))

    skills_list = [s.skill_name for s in Skill.query.filter_by(user_id=current_user.id).all()]
    skills_str = ", ".join(skills_list)
    return render_template('user/profile.html', profile=user_prof, skills_str=skills_str)


@user_bp.route('/resume_analyzer', methods=['GET', 'POST'])
@login_required
def resume_analyzer():
    user_prof = UserProfile.query.filter_by(user_id=current_user.id).first()
    analysis_result = None

    if request.method == 'POST':
        if 'resume' not in request.files:
            flash('No file uploaded.', 'danger')
            return redirect(url_for('user.resume_analyzer'))

        file = request.files['resume']
        if file.filename == '':
            flash('No selected file.', 'warning')
            return redirect(url_for('user.resume_analyzer'))

        if file and file.filename.lower().endswith('.pdf'):
            filename = secure_filename(f"user_{current_user.id}_{file.filename}")
            filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
            file.save(filepath)

            if user_prof:
                user_prof.resume_path = filepath
                db.session.commit()

            analysis_result = parse_pdf_resume(filepath)
            log_activity(current_user.id, 'Resume Uploaded & Analyzed', f'Resume file: {filename}')
            flash('Resume parsed and analyzed successfully!', 'success')
        else:
            flash('Please upload a valid PDF document.', 'danger')

    return render_template('user/resume_analyzer.html', profile=user_prof, analysis=analysis_result)


@user_bp.route('/chatbot')
@login_required
def chatbot():
    return render_template('user/chatbot.html')


@user_bp.route('/api/chat', methods=['POST'])
@login_required
def chat_api():
    data = request.get_json() or {}
    user_message = data.get('message', '')
    if not user_message:
        return jsonify({'response': 'Please enter a valid question.'})

    bot_reply = generate_chat_response(user_message)
    return jsonify({'response': bot_reply})
