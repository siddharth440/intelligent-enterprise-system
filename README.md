# Intelligent Expertise System (AI-Powered Platform)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask_3.0-green.svg)](https://flask.palletsprojects.com/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-orange.svg)](https://scikit-learn.org/)
[![Database](https://img.shields.io/badge/ORM-SQLAlchemy--MySQL-blueviolet.svg)](https://www.sqlalchemy.org/)

An enterprise-grade, production-ready AI-powered web application that analyzes a user's profile, skills, education, experience, interests, and PDF resume to accurately predict their area of tech expertise using Machine Learning. Provides personalized career growth roadmaps, recommended courses, certifications, projects, internships, and job opportunities.

---

## 🌟 Key Features & Modules

1. **Landing Page**: Professional glassmorphic design with Hero section, About project, Core features, Benefits, Team showcase, and Contact form.
2. **User Authentication**: Secure Registration, Login, Logout, Forgot Password, Password Hashing via `werkzeug.security`, and Session Management with Flask-Login.
3. **User Profile & Skill Matrix**: Comprehensive user profiling capturing education, college, department, experience, project counts, programming languages, and skills.
4. **AI Expertise Prediction**: Multi-model Machine Learning pipeline (Random Forest, Decision Tree, Naive Bayes) predicting expertise across 12 domains:
   - *Artificial Intelligence, Machine Learning, Data Science, Web Development, Mobile Development, Cyber Security, Cloud Computing, DevOps, UI/UX Design, Software Development, Networking, Database Administration.*
5. **Recommendation Engine**: Automatically generates personalized recommendations for:
   - Courses & Certifications
   - Industry Projects
   - Internships & Job Openings
   - 4-Week Skill Improvement Roadmap
6. **PDF Resume Analyzer**: Upload PDF resumes for automated text parsing via `pdfplumber`/`PyPDF2`, skill extraction, experience calculation, missing skill detection, and formatting recommendations.
7. **AI Chat Assistant**: Dynamic interactive career chatbot providing technical advice, interview preparation tips, and learning roadmaps.
8. **Admin Control Center**: Role-Based Access Control (RBAC) allowing admins to manage user accounts, trigger ML model dataset generation & retraining, and inspect audit logs.
9. **Visual Analytics Dashboard**: Interactive Chart.js graphs visualizing domain distributions, skill frequency heatmaps, model comparisons, and job market trends.
10. **PDF Report Downloads**: Downloadable PDF summaries for Expertise Predictions, Skills Analysis, Recommendations, and Resume Parsing via `ReportLab`.

---

## 🏗️ Project Architecture

```
/Intelligent_Expertise_System
│
├── app.py                      # Flask Application Entry Point & Route Loader
├── config.py                   # Global Configuration (DB, Uploads, Models)
├── requirements.txt            # Python Dependencies
├── README.md                   # Project Documentation
├── database/
│   ├── schema.sql              # MySQL Pure DDL Table Creation Script
│   └── seed_data.sql           # Initial Database Seed Script
├── models/
│   └── db_models.py            # SQLAlchemy ORM Database Models (12 Tables)
├── routes/
│   ├── main_routes.py          # Home, About, Contact
│   ├── auth_routes.py          # Authentication & Session Management
│   ├── user_routes.py          # Dashboard, Profile, Skills
│   ├── ai_routes.py            # AI Prediction & Recommendation API
│   ├── admin_routes.py         # Admin Controls & Model Retraining
│   ├── analytics_routes.py     # Analytics & Chart Data APIs
│   └── report_routes.py       # Downloadable PDF Export Engine
├── ai_model/
│   ├── generate_dataset.py     # Synthesizes 5,000+ Developer Records
│   ├── train_model.py          # Multi-Model ML Training Pipeline
│   ├── predict.py              # ML Inference Engine
│   ├── expertise_model.pkl     # Pre-Trained Random Forest Classifier
│   ├── vectorizer.pkl         # Saved TF-IDF Feature Vectorizer
│   └── label_encoder.pkl      # Saved Domain Label Encoder
├── utils/
│   ├── resume_parser.py        # PDF Resume Extraction Engine
│   ├── chatbot_engine.py       # AI Chat Assistant Engine
│   ├── report_generator.py     # PDF Export Engine
│   └── helpers.py              # Activity Logging & Security Utilities
├── static/
│   ├── css/main.css            # Custom Glassmorphic Dark UI Theme
│   └── js/
│       ├── main.js             # Theme Switcher & UI Helpers
│       ├── analytics_charts.js # Chart.js Canvas Visualizations
│       └── chatbot.js          # Interactive Chat Assistant UI
├── templates/                  # Modular HTML5 Templates
├── datasets/                   # Synthesized CSV Datasets (5000+ rows)
├── uploads/                    # PDF Resumes Storage
└── reports/                    # Generated Export PDFs
```

---

## 🛠️ Tech Stack

- **Backend**: Python 3.10+, Flask
- **Database / ORM**: MySQL / SQLite, SQLAlchemy ORM, PyMySQL
- **AI / ML**: Scikit-Learn, Pandas, NumPy, Joblib, TF-IDF Vectorization
- **Authentication**: Flask-Login, Werkzeug Security
- **Frontend**: HTML5, CSS3 Glassmorphic Styling, JavaScript (ES6)
- **Charts & Visualizations**: Chart.js
- **PDF Report Generation**: ReportLab / PyPDF2 / pdfplumber

---

## 🚀 Quick Setup & Installation Guide

### Step 1: Clone / Navigate to Directory
```bash
cd Intelligent_Expertise_System
```

### Step 2: Create & Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Application
```bash
python app.py
```
> **Note**: On startup, the application will automatically create all database tables (SQLite by default or MySQL if configured), seed sample courses/certs/admin accounts, synthesize 5,000+ user records, and train the Random Forest ML classifier!

Open your browser and navigate to: **`http://127.0.0.1:5000`**

---

## 🗄️ Database Setup Options

### Option A: Automatic Local Run (SQLite Zero-Config - Default)
The application will automatically initialize `database/app.db` without requiring an external MySQL server installation.

### Option B: MySQL Production Setup
1. Open MySQL workbench or terminal and run `database/schema.sql` and `database/seed_data.sql`.
2. Set environment variables before running `app.py`:
```bash
export USE_MYSQL=True
export MYSQL_USER=root
export MYSQL_PASSWORD=your_password
export MYSQL_HOST=localhost
export MYSQL_DB=intelligent_expertise_db
```

---

## 🔑 Default Administrator Credentials

- **Email**: `admin@expertise.ai`
- **Password**: `Admin@123`

---

## 🧪 Testing ML Pipeline Execution

You can manually trigger dataset generation and model retraining via CLI:
```bash
# 1. Generate 5,000+ user dataset
python ai_model/generate_dataset.py

# 2. Train Random Forest, Decision Tree & Naive Bayes classifiers
python ai_model/train_model.py
```

---

## 📜 License
Developed for educational & hackathon demonstration purposes. Open source under the MIT License.
