-- ========================================================
-- Intelligent Expertise System Seed Data Script
-- Initial Data Population for Courses, Certifications, Projects, Jobs & Admin
-- ========================================================

USE intelligent_expertise_db;

-- Insert Admin Account (Password: Admin@123)
-- Hash generated via Werkzeug generate_password_hash
INSERT IGNORE INTO users (id, full_name, email, password_hash, role) VALUES 
(1, 'System Administrator', 'admin@expertise.ai', 'scrypt:32768:8:1$K3Jz6tX2nQ0v9Y1m$3a510a7cb54c424a6e8df81bf052843efc6ef6e61fbbcf0927dfa60df64bf4593818e3dd4fd97ae54019a557ea78ae073ae0d970aa43cfaeb575bf4240763a8a', 'admin');

-- Insert Sample Courses
INSERT INTO courses (title, domain, level, provider, url, duration) VALUES
('Deep Learning Specialization', 'Artificial Intelligence', 'Advanced', 'Coursera / DeepLearning.AI', 'https://coursera.org/specializations/deep-learning', '3 Months'),
('Machine Learning A-Z: AI, Python & R', 'Machine Learning', 'Beginner', 'Udemy', 'https://udemy.com/course/machinelearning', '40 Hours'),
('Applied Data Science with Python', 'Data Science', 'Intermediate', 'Coursera / Univ of Michigan', 'https://coursera.org/specializations/data-science-python', '4 Months'),
('The Complete 2026 Web Development Bootcamp', 'Web Development', 'Beginner', 'Udemy', 'https://udemy.com/course/the-complete-web-development-bootcamp', '65 Hours'),
('Flutter & Dart - The Complete Guide', 'Mobile Development', 'Intermediate', 'Udemy', 'https://udemy.com/course/learn-flutter-dart-to-build-ios-android-apps', '42 Hours'),
('Certified Ethical Hacker (CEH) Master Prep', 'Cyber Security', 'Advanced', 'EC-Council / Cybrary', 'https://cybrary.it/course/certified-ethical-hacker', '50 Hours'),
('AWS Certified Solutions Architect Associate', 'Cloud Computing', 'Intermediate', 'A Cloud Guru', 'https://acloudguru.com/course/aws-certified-solutions-architect-associate', '30 Hours'),
('Docker and Kubernetes: The Complete Guide', 'DevOps', 'Intermediate', 'Udemy', 'https://udemy.com/course/docker-and-kubernetes-the-complete-guide', '22 Hours'),
('Google UX Design Professional Certificate', 'UI/UX Design', 'Beginner', 'Coursera / Google', 'https://coursera.org/professional-certificates/google-ux-design', '6 Months'),
('Complete Python Developer: Zero to Mastery', 'Software Development', 'Intermediate', 'Zero To Mastery', 'https://zerotomastery.io/courses/learn-python', '35 Hours');

-- Insert Sample Certifications
INSERT INTO certifications (title, domain, issuing_body, level, url) VALUES
('TensorFlow Developer Certificate', 'Artificial Intelligence', 'Google', 'Intermediate', 'https://www.tensorflow.org/certificate'),
('AWS Certified Machine Learning - Specialty', 'Machine Learning', 'Amazon Web Services', 'Advanced', 'https://aws.amazon.com/certification/certified-machine-learning-specialty'),
('IBM Data Science Professional Certificate', 'Data Science', 'IBM', 'Beginner', 'https://coursera.org/professional-certificates/ibm-data-science'),
('Meta Front-End Developer Professional Certificate', 'Web Development', 'Meta', 'Intermediate', 'https://coursera.org/professional-certificates/meta-front-end-developer'),
('CompTIA Security+ (SY0-701)', 'Cyber Security', 'CompTIA', 'Intermediate', 'https://www.comptia.org/certifications/security'),
('Certified Kubernetes Administrator (CKA)', 'DevOps', 'Linux Foundation / CNCF', 'Advanced', 'https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka');

-- Insert Sample Projects
INSERT INTO projects (title, domain, difficulty, tech_stack, description) VALUES
('Real-time Object Detection & Tracking System', 'Artificial Intelligence', 'Advanced', 'Python, YOLOv8, OpenCV, PyTorch', 'Build an AI computer vision application for automated multi-object video stream analytics.'),
('Predictive Customer Churn Analytics Pipeline', 'Machine Learning', 'Intermediate', 'Python, Scikit-Learn, Pandas, Flask', 'End-to-end ML model pipeline predicting subscription cancellation risks with web dashboard.'),
('Cloud Native Microservices E-Commerce API', 'Cloud Computing', 'Advanced', 'Docker, Kubernetes, AWS EKS, Go, PostgreSQL', 'Containerized microservices architecture with distributed tracing and auto-scaling.'),
('DevOps CI/CD Automated Pipeline Infrastructure', 'DevOps', 'Intermediate', 'Jenkins, Terraform, Ansible, GitHub Actions', 'Automated GitOps pipeline deploying containerized Flask applications to AWS.'),
('Full-Stack Real-Time Collaborative Canvas', 'Web Development', 'Intermediate', 'React, Node.js, WebSockets, TailwindCSS', 'Interactive whiteboarding platform with multi-user real-time cursor sync.');

-- Insert Sample Jobs & Internships
INSERT INTO jobs (title, company, domain, location, job_type, url) VALUES
('AI Research Intern', 'OpenAI Research Lab', 'Artificial Intelligence', 'San Francisco, CA / Remote', 'Internship', 'https://careers.openai.com'),
('Junior Machine Learning Engineer', 'Databricks', 'Machine Learning', 'New York, NY', 'Full-Time', 'https://databricks.com/company/careers'),
('Data Analyst Intern', 'Snowflake', 'Data Science', 'Austin, TX', 'Internship', 'https://snowflake.com/careers'),
('Full Stack Web Developer', 'Vercel', 'Web Development', 'Remote', 'Full-Time', 'https://vercel.com/careers'),
('Cyber Security SOC Analyst', 'CrowdStrike', 'Cyber Security', 'Remote', 'Full-Time', 'https://crowdstrike.com/careers'),
('Cloud Infrastructure Engineer', 'AWS Infrastructure Team', 'Cloud Computing', 'Seattle, WA', 'Full-Time', 'https://amazon.jobs');
