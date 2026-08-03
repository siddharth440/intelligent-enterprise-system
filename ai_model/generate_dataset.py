import os
import random
import pandas as pd
import numpy as np

# Define 12 Core Tech Domains and associated keywords
DOMAINS_KEYWORD_MAP = {
    'Artificial Intelligence': {
        'skills': ['PyTorch', 'TensorFlow', 'Neural Networks', 'Computer Vision', 'NLP', 'Deep Learning', 'Generative AI', 'LLMs', 'Transformers', 'Reinforcement Learning', 'Keras', 'OpenCV'],
        'languages': ['Python', 'C++', 'Julia'],
        'interests': ['Robotics', 'Apostle AI', 'Autonomous Systems', 'Speech Recognition', 'Cognitive Computing']
    },
    'Machine Learning': {
        'skills': ['Scikit-Learn', 'Pandas', 'NumPy', 'Supervised Learning', 'Unsupervised Learning', 'XGBoost', 'Feature Engineering', 'Model Deployment', 'Statsmodels', 'Classification', 'Regression'],
        'languages': ['Python', 'R', 'MATLAB'],
        'interests': ['Predictive Analytics', 'Pattern Recognition', 'Data Mining', 'Algorithmic Trading']
    },
    'Data Science': {
        'skills': ['Data Visualization', 'SQL', 'Tableau', 'Power BI', 'Exploratory Data Analysis', 'Statistical Analysis', 'Big Data', 'Spark', 'Hadoop', 'Data Pipelines', 'Seaborn'],
        'languages': ['Python', 'R', 'SQL', 'SAS'],
        'interests': ['Business Intelligence', 'Data Strategy', 'Customer Insights', 'Data Wrangling']
    },
    'Web Development': {
        'skills': ['HTML5', 'CSS3', 'JavaScript', 'React.js', 'Vue.js', 'Node.js', 'Express.js', 'Flask', 'Django', 'REST APIs', 'TailwindCSS', 'TypeScript', 'GraphQL'],
        'languages': ['JavaScript', 'TypeScript', 'HTML/CSS', 'Python', 'PHP'],
        'interests': ['Full Stack Development', 'UI Responsiveness', 'Web Performance', 'Single Page Apps']
    },
    'Mobile Development': {
        'skills': ['Flutter', 'React Native', 'Android Studio', 'Swift', 'Kotlin', 'iOS Development', 'Mobile UI', 'SQLite', 'Firebase', 'App Store Deployment', 'Core Data'],
        'languages': ['Kotlin', 'Swift', 'Dart', 'Java', 'JavaScript'],
        'interests': ['Cross-Platform Apps', 'Mobile Security', 'App UX Design', 'Location-Based Services']
    },
    'Cyber Security': {
        'skills': ['Ethical Hacking', 'Penetration Testing', 'Network Security', 'Cryptography', 'SIEM', 'Wireshark', 'Metasploit', 'Vulnerability Assessment', 'Firewalls', 'Incident Response', 'Identity Management'],
        'languages': ['Python', 'Bash', 'C', 'Assembly', 'PowerShell'],
        'interests': ['Zero Trust Architecture', 'Malware Analysis', 'Forensics', 'Bug Bounty']
    },
    'Cloud Computing': {
        'skills': ['AWS', 'Microsoft Azure', 'Google Cloud Platform', 'Cloud Architecture', 'Serverless', 'Lambda', 'S3', 'EC2', 'Cloud Security', 'IAM', 'Terraform'],
        'languages': ['Python', 'Bash', 'Go', 'YAML', 'JSON'],
        'interests': ['Hybrid Cloud', 'Cloud Migration', 'Cost Optimization', 'High Availability']
    },
    'DevOps': {
        'skills': ['Docker', 'Kubernetes', 'CI/CD', 'Jenkins', 'GitHub Actions', 'Ansible', 'Terraform', 'Prometheus', 'Grafana', 'Infrastructure as Code', 'Linux Admin'],
        'languages': ['Bash', 'Python', 'Go', 'YAML'],
        'interests': ['Site Reliability Engineering', 'Automation', 'Containerization', 'Microservices Monitoring']
    },
    'UI/UX Design': {
        'skills': ['Figma', 'Adobe XD', 'Wireframing', 'Prototyping', 'User Research', 'Usability Testing', 'Design Systems', 'Interaction Design', 'Information Architecture', 'Visual Design'],
        'languages': ['HTML/CSS', 'JavaScript'],
        'interests': ['User Centered Design', 'Accessibility Design', 'Design Thinking', 'Micro-interactions']
    },
    'Software Development': {
        'skills': ['Object-Oriented Programming', 'Data Structures', 'Algorithms', 'Design Patterns', 'Git', 'Agile/Scrum', 'Unit Testing', 'Refactoring', 'System Architecture'],
        'languages': ['Java', 'C++', 'C#', 'Python', 'Go'],
        'interests': ['Enterprise Applications', 'Clean Code', 'Performance Tuning', 'Distributed Systems']
    },
    'Networking': {
        'skills': ['TCP/IP', 'Cisco Packet Tracer', 'Routing & Switching', 'DNS', 'DHCP', 'LAN/WAN', 'CCNA', 'Network Diagnostics', 'VPNs', 'Network Monitoring', 'Subnetting'],
        'languages': ['Bash', 'Python', 'Tcl'],
        'interests': ['Software-Defined Networking', 'Network Virtualization', '5G Infrastructure', 'Fiber Optics']
    },
    'Database Administration': {
        'skills': ['MySQL', 'PostgreSQL', 'Oracle DB', 'MongoDB', 'Query Optimization', 'Database Indexing', 'Replication', 'Backup & Recovery', 'Database Design', 'Redis', 'Cassandra'],
        'languages': ['SQL', 'PL/SQL', 'Python', 'Bash'],
        'interests': ['NoSQL Architecture', 'High Availability Databases', 'Data Warehousing', 'Transaction Security']
    }
}

DEGREES = ['B.Tech Computer Science', 'B.Tech Information Technology', 'B.Tech AI & Data Science', 'BCA', 'MCA', 'M.Tech Computer Science', 'B.Sc Computer Science']

def generate_synthetic_dataset(num_records=5000, output_path='datasets/expertise_dataset.csv'):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    records = []
    
    domains = list(DOMAINS_KEYWORD_MAP.keys())
    
    for i in range(num_records):
        # Pick primary domain
        primary_domain = random.choice(domains)
        domain_info = DOMAINS_KEYWORD_MAP[primary_domain]
        
        # Select 3-6 core skills from target domain
        core_skills = random.sample(domain_info['skills'], min(len(domain_info['skills']), random.randint(3, 6)))
        
        # Optionally add 1-2 random secondary skills from other domains (noise/cross-disciplinary)
        other_domains = [d for d in domains if d != primary_domain]
        secondary_domain = random.choice(other_domains)
        noise_skills = random.sample(DOMAINS_KEYWORD_MAP[secondary_domain]['skills'], random.randint(0, 2))
        
        all_skills = core_skills + noise_skills
        random.shuffle(all_skills)
        skills_str = ", ".join(all_skills)
        
        # Languages
        langs = random.sample(domain_info['languages'], min(len(domain_info['languages']), random.randint(1, 3)))
        langs_str = ", ".join(langs)
        
        # Interests
        interests = random.sample(domain_info['interests'], min(len(domain_info['interests']), random.randint(1, 2)))
        interests_str = ", ".join(interests)
        
        # Numerical features realistic for domain profile
        exp_years = random.choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 10], weights=[25, 20, 15, 15, 10, 5, 4, 3, 2, 1])[0]
        projects_count = random.randint(1, 12) + (exp_years // 2)
        certs_count = random.randint(0, 5)
        education = random.choice(DEGREES)
        
        # Combined text feature for NLP classification
        combined_text = f"Skills: {skills_str}. Languages: {langs_str}. Interests: {interests_str}. Education: {education}."
        
        records.append({
            'user_id': 1000 + i,
            'skills_text': combined_text,
            'skills_list': skills_str,
            'programming_languages': langs_str,
            'interests': interests_str,
            'education': education,
            'experience_years': exp_years,
            'projects_count': projects_count,
            'certifications_count': certs_count,
            'target_domain': primary_domain
        })
        
    df = pd.DataFrame(records)
    df.to_csv(output_path, index=False)
    print(f"[SUCCESS] Dataset successfully generated with {len(df)} records at: {output_path}")
    return df

if __name__ == '__main__':
    generate_synthetic_dataset(num_records=5200)
