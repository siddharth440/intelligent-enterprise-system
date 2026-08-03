from models.db_models import db, ActivityLog, AdminLog
from flask import request

def log_activity(user_id, activity_type, details=""):
    """
    Logs user activity to activity_logs table
    """
    try:
        log = ActivityLog(user_id=user_id, activity_type=activity_type, details=details)
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        db.session.rollback()

def log_admin_action(user_id, action):
    """
    Logs administrative action to admin_logs table
    """
    try:
        ip = request.remote_addr if request else '127.0.0.1'
        log = AdminLog(user_id=user_id, action=action, ip_address=ip)
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
