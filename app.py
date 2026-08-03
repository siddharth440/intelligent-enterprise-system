import os
import json
from dotenv import load_dotenv
from flask import Flask, render_template
from config import Config
from models.db_models import db, User, Course, Certification, Project, Job
from flask_login import LoginManager

load_dotenv()

# Import Blueprints
from routes.main_routes import main_bp
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.ai_routes import ai_bp
from routes.admin_routes import admin_bp
from routes.analytics_routes import analytics_bp
from routes.report_routes import report_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'
    login_manager.init_app(app) 

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(report_bp)

    # Initialize Database Tables & Seed Initial Data
    with app.app_context():
        db.create_all()
        _seed_initial_data()
        _ensure_ml_model_trained()

    return app


def _seed_initial_data():
    """Seeds default admin account and course catalog if database is empty"""
    admin_email = os.environ.get('DEFAULT_ADMIN_EMAIL', 'admin@expertise.ai')
    admin_password = os.environ.get('DEFAULT_ADMIN_PASSWORD', 'Admin@123')

    admin = User.query.filter_by(email=admin_email).first()
    if not admin:
        admin = User(full_name='System Administrator', email=admin_email, role='admin')
        admin.set_password(admin_password)
        db.session.add(admin)
        db.session.commit()

    # 2. Default Catalog Items if empty
    if Course.query.count() == 0:
        sample_courses = [
            Course(title='Deep Learning Specialization', domain='Artificial Intelligence', level='Advanced', provider='Coursera / DeepLearning.AI', url='https://coursera.org/specializations/deep-learning', duration='3 Months'),
            Course(title='Machine Learning A-Z: AI, Python & R', domain='Machine Learning', level='Beginner', provider='Udemy', url='https://udemy.com/course/machinelearning', duration='40 Hours'),
            Course(title='Applied Data Science with Python', domain='Data Science', level='Intermediate', provider='Coursera / Univ of Michigan', url='https://coursera.org/specializations/data-science-python', duration='4 Months'),
            Course(title='The Complete 2026 Web Development Bootcamp', domain='Web Development', level='Beginner', provider='Udemy', url='https://udemy.com/course/the-complete-web-development-bootcamp', duration='65 Hours'),
            Course(title='Flutter & Dart - The Complete Guide', domain='Mobile Development', level='Intermediate', provider='Udemy', url='https://udemy.com/course/learn-flutter-dart-to-build-ios-android-apps', duration='42 Hours'),
            Course(title='Certified Ethical Hacker (CEH) Master Prep', domain='Cyber Security', level='Advanced', provider='EC-Council', url='https://cybrary.it/course/certified-ethical-hacker', duration='50 Hours'),
            Course(title='AWS Certified Solutions Architect Associate', domain='Cloud Computing', level='Intermediate', provider='A Cloud Guru', url='https://acloudguru.com/course/aws-certified-solutions-architect-associate', duration='30 Hours'),
            Course(title='Docker and Kubernetes: The Complete Guide', domain='DevOps', level='Intermediate', provider='Udemy', url='https://udemy.com/course/docker-and-kubernetes-the-complete-guide', duration='22 Hours'),
            Course(title='Google UX Design Professional Certificate', domain='UI/UX Design', level='Beginner', provider='Coursera / Google', url='https://coursera.org/professional-certificates/google-ux-design', duration='6 Months'),
            Course(title='Complete Python Developer: Zero to Mastery', domain='Software Development', level='Intermediate', provider='Zero To Mastery', url='https://zerotomastery.io/courses/learn-python', duration='35 Hours')
        ]
        db.session.add_all(sample_courses)

    if Certification.query.count() == 0:
        sample_certs = [
            Certification(title='TensorFlow Developer Certificate', domain='Artificial Intelligence', issuing_body='Google', level='Intermediate', url='https://www.tensorflow.org/certificate'),
            Certification(title='AWS Certified Machine Learning - Specialty', domain='Machine Learning', issuing_body='Amazon Web Services', level='Advanced', url='https://aws.amazon.com/certification/certified-machine-learning-specialty'),
            Certification(title='IBM Data Science Professional Certificate', domain='Data Science', issuing_body='IBM', level='Beginner', url='https://coursera.org/professional-certificates/ibm-data-science'),
            Certification(title='Meta Front-End Developer Professional Certificate', domain='Web Development', issuing_body='Meta', level='Intermediate', url='https://coursera.org/professional-certificates/meta-front-end-developer'),
            Certification(title='CompTIA Security+ (SY0-701)', domain='Cyber Security', issuing_body='CompTIA', level='Intermediate', url='https://www.comptia.org/certifications/security'),
            Certification(title='Certified Kubernetes Administrator (CKA)', domain='DevOps', issuing_body='Linux Foundation / CNCF', level='Advanced', url='https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka')
        ]
        db.session.add_all(sample_certs)

    if Project.query.count() == 0:
        sample_projects = [
            Project(title='Real-time Object Detection & Tracking System', domain='Artificial Intelligence', difficulty='Advanced', tech_stack='Python, YOLOv8, OpenCV, PyTorch', description='Build an AI computer vision application for automated video stream analytics.'),
            Project(title='Predictive Customer Churn Analytics Pipeline', domain='Machine Learning', difficulty='Intermediate', tech_stack='Python, Scikit-Learn, Pandas, Flask', description='End-to-end ML pipeline predicting customer cancellation risk with web dashboard.'),
            Project(title='Cloud Native Microservices E-Commerce API', domain='Cloud Computing', difficulty='Advanced', tech_stack='Docker, Kubernetes, AWS EKS, PostgreSQL', description='Containerized microservices architecture with distributed tracing and auto-scaling.'),
            Project(title='DevOps CI/CD Automated Pipeline Infrastructure', domain='DevOps', difficulty='Intermediate', tech_stack='Jenkins, Terraform, Ansible, GitHub Actions', description='Automated GitOps pipeline deploying Flask applications to cloud.'),
            Project(title='Full-Stack Real-Time Collaborative Canvas', domain='Web Development', difficulty='Intermediate', tech_stack='React, Node.js, WebSockets, TailwindCSS', description='Interactive whiteboarding platform with multi-user real-time cursor sync.')
        ]
        db.session.add_all(sample_projects)

    if Job.query.count() == 0:
        sample_jobs = [
            Job(title='AI Research Intern', company='OpenAI Research Lab', domain='Artificial Intelligence', location='Remote / San Francisco', job_type='Internship', url='https://careers.openai.com'),
            Job(title='Junior Machine Learning Engineer', company='Databricks', domain='Machine Learning', location='Austin, TX', job_type='Full-Time', url='https://databricks.com/company/careers'),
            Job(title='Data Analyst Intern', company='Snowflake', domain='Data Science', location='Remote', job_type='Internship', url='https://snowflake.com/careers'),
            Job(title='Full Stack Web Developer', company='Vercel', domain='Web Development', location='Remote', job_type='Full-Time', url='https://vercel.com/careers'),
            Job(title='Cyber Security SOC Analyst', company='CrowdStrike', domain='Cyber Security', location='Remote', job_type='Full-Time', url='https://crowdstrike.com/careers'),
            Job(title='Cloud Infrastructure Engineer', company='AWS Infrastructure Team', domain='Cloud Computing', location='Seattle, WA', job_type='Full-Time', url='https://amazon.jobs')
        ]
        db.session.add_all(sample_jobs)

    db.session.commit()


def _ensure_ml_model_trained():
    """Generates synthetic dataset and trains Random Forest model if not already present"""
    model_path = os.path.join(Config.AI_MODEL_FOLDER, 'expertise_model.pkl')
    dataset_path = os.path.join(Config.DATASET_FOLDER, 'expertise_dataset.csv')

    if not os.path.exists(model_path):
        print("[*] Pre-trained AI model not found. Generating dataset and training model...")
        from ai_model.generate_dataset import generate_synthetic_dataset
        from ai_model.train_model import train_and_evaluate
        
        generate_synthetic_dataset(num_records=5200, output_path=dataset_path)
        train_and_evaluate(dataset_path=dataset_path, model_dir=Config.AI_MODEL_FOLDER)


app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', '1').lower() in {'1', 'true', 'yes'}
    print(f"[*] Starting Intelligent Expertise System on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
