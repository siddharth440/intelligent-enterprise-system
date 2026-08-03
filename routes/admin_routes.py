import os
import json
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models.db_models import db, User, Prediction, AdminLog, ActivityLog, Feedback
from ai_model.train_model import train_and_evaluate
from utils.helpers import log_admin_action
from config import Config

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(func):
    """Decorator to enforce Admin Role-Based Access Control"""
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Access Denied. Administrative privileges required.', 'danger')
            return redirect(url_for('user.dashboard'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_users = User.query.filter_by(role='user').count()
    total_predictions = Prediction.query.count()
    feedbacks_count = Feedback.query.count()
    recent_logs = AdminLog.query.order_by(AdminLog.timestamp.desc()).limit(8).all()
    
    # Read ML model metrics file if exists
    metrics_path = os.path.join(Config.AI_MODEL_FOLDER, 'model_metrics.json')
    model_metrics = None
    if os.path.exists(metrics_path):
        try:
            with open(metrics_path, 'r') as f:
                model_metrics = json.load(f)
        except Exception:
            pass

    return render_template('admin/dashboard.html', 
                           total_users=total_users, 
                           total_predictions=total_predictions, 
                           feedbacks_count=feedbacks_count, 
                           recent_logs=recent_logs,
                           metrics=model_metrics)


@admin_bp.route('/users')
@login_required
@admin_required
def user_management():
    users_list = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/user_management.html', users=users_list)


@admin_bp.route('/users/toggle/<int:user_id>')
@login_required
@admin_required
def toggle_user_status(user_id):
    u = User.query.get_or_404(user_id)
    if u.id == current_user.id:
        flash('Cannot deactivate your own admin account.', 'warning')
        return redirect(url_for('admin.user_management'))
        
    u.is_active = not u.is_active
    db.session.commit()
    log_admin_action(current_user.id, f"Toggled status for User ID {user_id} ({u.email}) to active={u.is_active}")
    flash(f"User {u.email} status updated.", 'info')
    return redirect(url_for('admin.user_management'))


@admin_bp.route('/users/delete/<int:user_id>')
@login_required
@admin_required
def delete_user(user_id):
    u = User.query.get_or_404(user_id)
    if u.id == current_user.id:
        flash('Cannot delete your own admin account.', 'danger')
        return redirect(url_for('admin.user_management'))

    db.session.delete(u)
    db.session.commit()
    log_admin_action(current_user.id, f"Deleted User ID {user_id} ({u.email})")
    flash('User deleted successfully.', 'success')
    return redirect(url_for('admin.user_management'))


@admin_bp.route('/retrain', methods=['GET', 'POST'])
@login_required
@admin_required
def retrain_model():
    if request.method == 'POST':
        try:
            metrics = train_and_evaluate(dataset_path=os.path.join(Config.DATASET_FOLDER, 'expertise_dataset.csv'),
                                         model_dir=Config.AI_MODEL_FOLDER)
            log_admin_action(current_user.id, f"Retrained ML Model: Accuracy {metrics.get('accuracy')}%")
            flash(f"Machine Learning Model successfully retrained! New Accuracy: {metrics.get('accuracy')}%", 'success')
        except Exception as e:
            flash(f"Model retraining failed: {str(e)}", 'danger')
        return redirect(url_for('admin.retrain_model'))

    metrics_path = os.path.join(Config.AI_MODEL_FOLDER, 'model_metrics.json')
    metrics = None
    if os.path.exists(metrics_path):
        with open(metrics_path, 'r') as f:
            metrics = json.load(f)

    return render_template('admin/retrain_model.html', metrics=metrics)
