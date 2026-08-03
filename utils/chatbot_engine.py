import re
import random

CAREER_FAQ = {
    r'hello|hi|hey|greetings': [
        "Hello! I am your AI Expertise & Career Assistant. How can I guide your tech journey today?",
        "Greetings! Ask me about career paths, interview prep, skill roadmaps, or resume optimization."
    ],
    r'ai|artificial intelligence|machine learning|data science': [
        "For AI/ML/Data Science: Master Python, NumPy, Pandas, Scikit-Learn, and PyTorch. Focus on building real-world projects such as predictive analytics, object detection, or LLM fine-tuning.",
        "Top certifications in AI/ML: TensorFlow Developer Certificate, AWS Machine Learning Specialty, and IBM Data Science Professional."
    ],
    r'web development|frontend|backend|full stack': [
        "Web Development Roadmap: HTML5/CSS3/JavaScript -> React/Vue.js -> Node.js/Flask -> MongoDB/PostgreSQL -> Docker & AWS deployment.",
        "Key advice: Build production-ready projects with responsive UI, secure REST APIs, and clean code documentation."
    ],
    r'cyber security|ethical hacking|security': [
        "Cyber Security Roadmap: Start with Networking (TCP/IP, Linux Admin) -> CompTIA Security+ -> Hands-on labs on TryHackMe/HackTheBox -> Certified Ethical Hacker (CEH) or OSCP.",
        "Focus areas: Vulnerability assessment, penetration testing, cryptography, and SIEM monitoring."
    ],
    r'cloud|devops|aws|docker|kubernetes': [
        "Cloud & DevOps Roadmap: Linux Admin -> Git & Bash -> Docker -> Kubernetes -> Terraform -> AWS/Azure Solutions Architect certification.",
        "Learn GitOps and CI/CD automation pipelines using GitHub Actions or Jenkins."
    ],
    r'interview|prepare|interview prep': [
        "Interview Preparation Checklist:\n1. Solve Data Structures & Algorithms on LeetCode/HackerRank.\n2. Prepare System Design basics (REST, Load Balancers, Caching).\n3. Rehearse the STAR method for behavioral questions.\n4. Review your project architecture thoroughly."
    ],
    r'resume|cv|portfolio': [
        "Resume Best Practices:\n- Keep it 1 page long for entry/mid-level positions.\n- Use actionable verbs and quantitative impacts (e.g., 'Reduced API latency by 35%').\n- Tailor keywords to the job description to pass ATS filters."
    ],
    r'roadmap|learning path|career growth': [
        "Career Growth Strategy:\n1. Complete your AI Profile Prediction to spot skill gaps.\n2. Follow our personalized Recommendation Engine for courses.\n3. Build 2-3 portfolio projects.\n4. Practice mock interviews and gain certifications."
    ]
}

DEFAULT_RESPONSES = [
    "That is a great career question! To give you the most accurate advice, ensure your profile and skills are updated in the system, then request an AI Expertise Analysis.",
    "Interesting query! Focusing on hands-on project portfolio building alongside core fundamentals is the fastest way to accelerate your tech career.",
    "For detailed domain roadmaps, check out our AI Recommendation Engine tab after completing your profile setup."
]

def generate_chat_response(user_query):
    query_clean = user_query.strip().lower()
    
    for pattern, responses in CAREER_FAQ.items():
        if re.search(pattern, query_clean):
            return random.choice(responses)
            
    return random.choice(DEFAULT_RESPONSES)
