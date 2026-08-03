-- ========================================================
-- Intelligent Expertise System Database Schema
-- Target Database: MySQL 8.0+
-- ========================================================

CREATE DATABASE IF NOT EXISTS intelligent_expertise_db;
USE intelligent_expertise_db;

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user', -- 'user' or 'admin'
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. User Profiles Table
CREATE TABLE IF NOT EXISTS user_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    phone VARCHAR(20),
    age INT,
    gender VARCHAR(20),
    education VARCHAR(100),
    college VARCHAR(150),
    department VARCHAR(100),
    programming_languages TEXT,
    experience_years INT DEFAULT 0,
    projects_count INT DEFAULT 0,
    interests TEXT,
    resume_path VARCHAR(255),
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 3. Skills Table
CREATE TABLE IF NOT EXISTS skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    skill_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) DEFAULT 'General',
    proficiency VARCHAR(30) DEFAULT 'Intermediate', -- 'Beginner', 'Intermediate', 'Advanced', 'Expert'
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 4. Predictions Table
CREATE TABLE IF NOT EXISTS predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    predicted_expertise VARCHAR(100) NOT NULL,
    confidence_score FLOAT NOT NULL,
    algorithm_used VARCHAR(50) DEFAULT 'Random Forest',
    strengths TEXT,
    weaknesses TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 5. Courses Table
CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    domain VARCHAR(100) NOT NULL,
    level VARCHAR(50) DEFAULT 'Beginner',
    provider VARCHAR(100),
    url VARCHAR(255),
    duration VARCHAR(50)
);

-- 6. Certifications Table
CREATE TABLE IF NOT EXISTS certifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    domain VARCHAR(100) NOT NULL,
    issuing_body VARCHAR(100),
    level VARCHAR(50) DEFAULT 'Intermediate',
    url VARCHAR(255)
);

-- 7. Projects Table
CREATE TABLE IF NOT EXISTS projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    domain VARCHAR(100) NOT NULL,
    difficulty VARCHAR(50) DEFAULT 'Intermediate',
    tech_stack TEXT,
    description TEXT
);

-- 8. Jobs Table
CREATE TABLE IF NOT EXISTS jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    company VARCHAR(100) NOT NULL,
    domain VARCHAR(100) NOT NULL,
    location VARCHAR(100),
    job_type VARCHAR(50) DEFAULT 'Full-Time', -- 'Full-Time', 'Internship', 'Remote'
    url VARCHAR(255)
);

-- 9. Recommendations Table
CREATE TABLE IF NOT EXISTS recommendations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    category VARCHAR(50) NOT NULL, -- 'Course', 'Certification', 'Project', 'Internship', 'Job'
    description TEXT,
    link VARCHAR(255),
    urgency VARCHAR(30) DEFAULT 'Medium',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 10. Admin Logs Table
CREATE TABLE IF NOT EXISTS admin_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action VARCHAR(255) NOT NULL,
    ip_address VARCHAR(45),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- 11. Feedback Table
CREATE TABLE IF NOT EXISTS feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    message TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 12. Activity Logs Table
CREATE TABLE IF NOT EXISTS activity_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    activity_type VARCHAR(100) NOT NULL,
    details TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
