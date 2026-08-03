import os
from flask import Blueprint, send_from_directory, flash, redirect, url_for
from flask_login import login_required, current_user
from models.db_models import Prediction, Recommendation, UserProfile
from utils.report_generator import generate_pdf_report
from utils.resume_parser import parse_pdf_resume
from config import Config

report_bp = Blueprint('report', __name__, url_prefix='/report')

@report_bp.route('/download/<report_type>')
@login_required
def download_report(report_type):
    valid_types = {'expertise': 'Expertise Report', 'skill': 'Skill Report', 'recommendation': 'Recommendation Report', 'resume': 'Resume Analysis Report'}
    
    if report_type not in valid_types:
        flash('Invalid report type requested.', 'danger')
        return redirect(url_for('user.dashboard'))

    formatted_title = valid_types[report_type]
    
    latest_pred = Prediction.query.filter_by(user_id=current_user.id).order_by(Prediction.created_at.desc()).first()
    recs = Recommendation.query.filter_by(user_id=current_user.id).all()
    user_prof = UserProfile.query.filter_by(user_id=current_user.id).first()

    resume_data = None
    if report_type == 'resume' and user_prof and user_prof.resume_path and os.path.exists(user_prof.resume_path):
        resume_data = parse_pdf_resume(user_prof.resume_path)

    filename = generate_pdf_report(
        user=current_user,
        prediction=latest_pred,
        resume_data=resume_data,
        recommendations=recs,
        report_type=formatted_title
    )

    return send_from_directory(Config.REPORT_FOLDER, filename, as_attachment=True)
