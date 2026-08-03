import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # MySQL connection string format: mysql+pymysql://username:password@localhost/db_name
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'root')
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'intelligent_expertise_db')
    
    # SQLite fallback path for zero-config local run if MySQL service is not available
    SQLITE_PATH = os.path.join(BASE_DIR, 'database', 'app.db')
    
    # Support Render/production database URLs first, then MySQL, then SQLite fallback
    if os.environ.get('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    elif os.environ.get('USE_MYSQL', '').lower() in ['true', '1']:
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
    else:
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{SQLITE_PATH}"
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File Paths
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    REPORT_FOLDER = os.path.join(BASE_DIR, 'reports')
    DATASET_FOLDER = os.path.join(BASE_DIR, 'datasets')
    AI_MODEL_FOLDER = os.path.join(BASE_DIR, 'ai_model')
    
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max resume upload
    
    # Ensure necessary folders exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(REPORT_FOLDER, exist_ok=True)
    os.makedirs(DATASET_FOLDER, exist_ok=True)
    os.makedirs(AI_MODEL_FOLDER, exist_ok=True)
