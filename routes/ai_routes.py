from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models.db_models import db, UserProfile, Skill, Prediction, Recommendation, Course, Certification, Project, Job
from ai_model.predict import predict_expertise
from utils.helpers import log_activity

ai_bp = Blueprint('ai', __name__, url_prefix='/ai')

@ai_bp.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    profile = UserProfile.query.filter_by(user_id=current_user.id).first()
    skills = Skill.query.filter_by(user_id=current_user.id).all()
    skills_text = ", ".join([s.skill_name for s in skills])

    if not skills_text and not (profile and profile.interests):
        flash('Please fill in your skills or profile interests before generating an AI prediction.', 'warning')
        return redirect(url_for('user.profile'))

    # Run AI Prediction
    result = predict_expertise(
        skills_text=skills_text,
        programming_languages=profile.programming_languages if profile else "",
        interests=profile.interests if profile else "",
        education=profile.education if profile else "",
        experience_years=profile.experience_years if profile else 0,
        projects_count=profile.projects_count if profile else 0
    )

    # Store Prediction in Database
    prediction_record = Prediction(
        user_id=current_user.id,
        predicted_expertise=result['predicted_expertise'],
        confidence_score=result['confidence_score'],
        algorithm_used=result['algorithm_used'],
        strengths=result['strengths'],
        weaknesses=result['weaknesses']
    )
    db.session.add(prediction_record)
    db.session.commit()

    # Generate Recommendations automatically for this predicted domain
    _generate_recommendations_for_user(current_user.id, result['predicted_expertise'], result['weaknesses'])

    log_activity(current_user.id, 'AI Prediction Executed', f"Domain: {result['predicted_expertise']} ({result['confidence_score']}%)")
    flash('AI Expertise Prediction completed successfully!', 'success')

    return render_template('user/prediction_result.html', prediction=prediction_record, top_domains=result['top_domains'])


@ai_bp.route('/recommendations')
@login_required
def recommendations():
    user_recs = Recommendation.query.filter_by(user_id=current_user.id).order_by(Recommendation.created_at.desc()).all()
    latest_pred = Prediction.query.filter_by(user_id=current_user.id).order_by(Prediction.created_at.desc()).first()

    return render_template('user/recommendations.html', recommendations=user_recs, prediction=latest_pred)


def _generate_recommendations_for_user(user_id, domain, weaknesses_str):
    """
    Queries catalog tables (courses, certs, projects, jobs) matching the predicted domain
    and inserts personalized recommendation records for the user.
    """
    Recommendation.query.filter_by(user_id=user_id).delete()

    matched_courses = Course.query.filter(Course.domain.ilike(f"%{domain}%")).limit(3).all()
    matched_certs = Certification.query.filter(Certification.domain.ilike(f"%{domain}%")).limit(2).all()
    matched_projects = Project.query.filter(Project.domain.ilike(f"%{domain}%")).limit(2).all()
    matched_jobs = Job.query.filter(Job.domain.ilike(f"%{domain}%")).limit(3).all()

    # Add Courses
    for c in matched_courses:
        rec = Recommendation(
            user_id=user_id,
            title=c.title,
            category='Course',
            description=f"Level: {c.level} | Provider: {c.provider} | Duration: {c.duration}",
            link=c.url,
            urgency='High'
        )
        db.session.add(rec)

    # Add Certifications
    for cert in matched_certs:
        rec = Recommendation(
            user_id=user_id,
            title=cert.title,
            category='Certification',
            description=f"Issuing Body: {cert.issuing_body} | Level: {cert.level}",
            link=cert.url,
            urgency='High'
        )
        db.session.add(rec)

    # Add Projects
    for p in matched_projects:
        rec = Recommendation(
            user_id=user_id,
            title=p.title,
            category='Project',
            description=f"Difficulty: {p.difficulty} | Stack: {p.tech_stack}. {p.description}",
            link="#",
            urgency='Medium'
        )
        db.session.add(rec)

    # Add Jobs & Internships
    for j in matched_jobs:
        rec = Recommendation(
            user_id=user_id,
            title=f"{j.title} at {j.company}",
            category='Internship' if 'Intern' in j.title or j.job_type == 'Internship' else 'Job',
            description=f"Location: {j.location} | Type: {j.job_type}",
            link=j.url,
            urgency='Medium'
        )
        db.session.add(rec)

    # Skill Improvement Plan item
    if weaknesses_str:
        db.session.add(Recommendation(
            user_id=user_id,
            title=f"Skill Improvement Roadmap: Address Gap Competencies",
            category='Skill Improvement Plan',
            description=f"Focus next 4 weeks on strengthening missing skills: {weaknesses_str}",
            link="#",
            urgency='High'
        ))

    db.session.commit()
