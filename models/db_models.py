from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')  # 'user' or 'admin'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    profile = db.relationship('UserProfile', backref='user', uselist=False, cascade="all, delete-orphan")
    skills = db.relationship('Skill', backref='user', lazy=True, cascade="all, delete-orphan")
    predictions = db.relationship('Prediction', backref='user', lazy=True, cascade="all, delete-orphan")
    recommendations = db.relationship('Recommendation', backref='user', lazy=True, cascade="all, delete-orphan")
    feedbacks = db.relationship('Feedback', backref='user', lazy=True, cascade="all, delete-orphan")
    activity_logs = db.relationship('ActivityLog', backref='user', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'


class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    education = db.Column(db.String(100), nullable=True)  # e.g., B.Tech, M.Tech, BCA, MCA
    college = db.Column(db.String(150), nullable=True)
    department = db.Column(db.String(100), nullable=True) # e.g., CS, IT, AI&DS, ECE
    programming_languages = db.Column(db.Text, nullable=True) # Comma separated
    experience_years = db.Column(db.Integer, default=0)
    projects_count = db.Column(db.Integer, default=0)
    interests = db.Column(db.Text, nullable=True)
    resume_path = db.Column(db.String(255), nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Skill(db.Model):
    __tablename__ = 'skills'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    skill_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), default='General')
    proficiency = db.Column(db.String(30), default='Intermediate') # Beginner, Intermediate, Advanced, Expert


class Prediction(db.Model):
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    predicted_expertise = db.Column(db.String(100), nullable=False)
    confidence_score = db.Column(db.Float, nullable=False)
    algorithm_used = db.Column(db.String(50), default='Random Forest')
    strengths = db.Column(db.Text, nullable=True)
    weaknesses = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    domain = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(50), default='Beginner')
    provider = db.Column(db.String(100), nullable=True)
    url = db.Column(db.String(255), nullable=True)
    duration = db.Column(db.String(50), nullable=True)


class Certification(db.Model):
    __tablename__ = 'certifications'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    domain = db.Column(db.String(100), nullable=False)
    issuing_body = db.Column(db.String(100), nullable=True)
    level = db.Column(db.String(50), default='Intermediate')
    url = db.Column(db.String(255), nullable=True)


class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    domain = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(50), default='Intermediate')
    tech_stack = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)


class Job(db.Model):
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    domain = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=True)
    job_type = db.Column(db.String(50), default='Full-Time')
    url = db.Column(db.String(255), nullable=True)


class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Course, Certification, Project, Internship, Job
    description = db.Column(db.Text, nullable=True)
    link = db.Column(db.String(255), nullable=True)
    urgency = db.Column(db.String(30), default='Medium')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class AdminLog(db.Model):
    __tablename__ = 'admin_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    action = db.Column(db.String(255), nullable=False)
    ip_address = db.Column(db.String(45), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    activity_type = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
