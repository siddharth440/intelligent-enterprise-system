import os
import joblib
import numpy as np
from config import Config

# Domain Taxonomy for Strengths and Weaknesses Evaluation
DOMAIN_EXPECTED_SKILLS = {
    'Artificial Intelligence': ['PyTorch', 'TensorFlow', 'Neural Networks', 'Computer Vision', 'NLP', 'Deep Learning', 'Generative AI', 'LLMs', 'OpenCV'],
    'Machine Learning': ['Scikit-Learn', 'Pandas', 'NumPy', 'Supervised Learning', 'Unsupervised Learning', 'XGBoost', 'Feature Engineering', 'Model Deployment'],
    'Data Science': ['SQL', 'Tableau', 'Power BI', 'Exploratory Data Analysis', 'Statistical Analysis', 'Big Data', 'Spark', 'Python'],
    'Web Development': ['HTML5', 'CSS3', 'JavaScript', 'React.js', 'Node.js', 'Express.js', 'Flask', 'REST APIs', 'TypeScript'],
    'Mobile Development': ['Flutter', 'React Native', 'Android Studio', 'Swift', 'Kotlin', 'iOS Development', 'Dart', 'Firebase'],
    'Cyber Security': ['Ethical Hacking', 'Penetration Testing', 'Network Security', 'Cryptography', 'Wireshark', 'Metasploit', 'Vulnerability Assessment'],
    'Cloud Computing': ['AWS', 'Microsoft Azure', 'Google Cloud Platform', 'Cloud Architecture', 'Lambda', 'Docker', 'Terraform'],
    'DevOps': ['Docker', 'Kubernetes', 'CI/CD', 'Jenkins', 'GitHub Actions', 'Ansible', 'Terraform', 'Linux Admin'],
    'UI/UX Design': ['Figma', 'Adobe XD', 'Wireframing', 'Prototyping', 'User Research', 'Usability Testing', 'Design Systems'],
    'Software Development': ['Object-Oriented Programming', 'Data Structures', 'Algorithms', 'Design Patterns', 'Git', 'Java', 'C++'],
    'Networking': ['TCP/IP', 'Cisco Packet Tracer', 'Routing & Switching', 'DNS', 'DHCP', 'LAN/WAN', 'CCNA'],
    'Database Administration': ['MySQL', 'PostgreSQL', 'Oracle DB', 'MongoDB', 'Query Optimization', 'Database Indexing', 'Redis']
}

_model = None
_vectorizer = None
_label_encoder = None

def _load_artifacts():
    global _model, _vectorizer, _label_encoder
    model_dir = Config.AI_MODEL_FOLDER
    
    model_path = os.path.join(model_dir, 'expertise_model.pkl')
    vec_path = os.path.join(model_dir, 'vectorizer.pkl')
    lbl_path = os.path.join(model_dir, 'label_encoder.pkl')
    
    if not (os.path.exists(model_path) and os.path.exists(vec_path) and os.path.exists(lbl_path)):
        # Retrain on demand if artifacts do not exist
        from ai_model.train_model import train_and_evaluate
        train_and_evaluate(model_dir=model_dir)
        
    _model = joblib.load(model_path)
    _vectorizer = joblib.load(vec_path)
    _label_encoder = joblib.load(lbl_path)

def predict_expertise(skills_text, programming_languages="", interests="", education="", experience_years=0, projects_count=0):
    """
    Predicts user expertise domain, confidence score, strengths, and missing skill weaknesses.
    """
    if _model is None:
        _load_artifacts()
        
    combined_input = f"Skills: {skills_text}. Languages: {programming_languages}. Interests: {interests}. Education: {education}."
    
    X_vec = _vectorizer.transform([combined_input]).toarray()
    
    # Predict probabilities
    probabilities = _model.predict_proba(X_vec)[0]
    best_idx = np.argmax(probabilities)
    
    predicted_domain = _label_encoder.inverse_transform([best_idx])[0]
    confidence_score = round(float(probabilities[best_idx]) * 100, 2)
    
    # Analyze strengths and weaknesses based on predicted domain
    user_skills_lower = [s.strip().lower() for s in (skills_text + ", " + programming_languages).split(",") if s.strip()]
    expected_skills = DOMAIN_EXPECTED_SKILLS.get(predicted_domain, [])
    
    strengths = []
    weaknesses = []
    
    for exp in expected_skills:
        if any(exp.lower() in us or us in exp.lower() for us in user_skills_lower):
            strengths.append(exp)
        else:
            weaknesses.append(exp)
            
    if not strengths:
        strengths = [f"Foundational understanding of {predicted_domain}"]
    if not weaknesses:
        weaknesses = [f"Advanced enterprise scaling in {predicted_domain}"]
        
    return {
        'predicted_expertise': predicted_domain,
        'confidence_score': confidence_score,
        'strengths': ", ".join(strengths[:5]),
        'weaknesses': ", ".join(weaknesses[:5]),
        'algorithm_used': 'Random Forest Classifier',
        'top_domains': [
            {'domain': _label_encoder.inverse_transform([idx])[0], 'probability': round(float(probabilities[idx]) * 100, 2)}
            for idx in np.argsort(probabilities)[::-1][:4]
        ]
    }
