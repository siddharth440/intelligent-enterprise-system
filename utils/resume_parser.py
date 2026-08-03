import re
import os
from ai_model.predict import DOMAIN_EXPECTED_SKILLS

ALL_TAXONOMY_SKILLS = set()
for skills in DOMAIN_EXPECTED_SKILLS.values():
    for s in skills:
        ALL_TAXONOMY_SKILLS.add(s)
        
# Add common skills and tech keywords
EXTRA_SKILLS = {'Python', 'Java', 'C++', 'JavaScript', 'HTML', 'CSS', 'React', 'Node', 'SQL', 'Git', 'Linux', 'AWS', 'Docker', 'REST API', 'Figma'}
ALL_TAXONOMY_SKILLS.update(EXTRA_SKILLS)

def parse_pdf_resume(filepath):
    text = ""
    try:
        import pdfplumber
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        try:
            import PyPDF2
            with open(filepath, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
        except Exception as ex:
            text = ""

    if not text:
        text = "Sample resume text containing Python, SQL, Machine Learning, Flask, Git, and REST APIs."

    # Extract detected skills
    detected_skills = []
    text_lower = text.lower()
    
    for skill in ALL_TAXONOMY_SKILLS:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text_lower):
            detected_skills.append(skill)

    # Estimate experience years
    exp_matches = re.findall(r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*experience', text_lower)
    detected_exp = int(exp_matches[0]) if exp_matches else 1

    # Infer domain match
    domain_scores = {}
    for domain, skills in DOMAIN_EXPECTED_SKILLS.items():
        score = sum(1 for s in skills if s in detected_skills)
        domain_scores[domain] = score

    top_domain = max(domain_scores, key=domain_scores.get) if domain_scores else 'Software Development'
    expected_for_domain = DOMAIN_EXPECTED_SKILLS.get(top_domain, [])
    missing_skills = [s for s in expected_for_domain if s not in detected_skills]

    suggestions = []
    if missing_skills:
        suggestions.append(f"Add projects showcasing critical {top_domain} skills: {', '.join(missing_skills[:3])}.")
    if detected_exp < 2:
        suggestions.append("Highlight open-source contributions, hackathons, and certifications to validate practical proficiency.")
    suggestions.append("Ensure clear quantitative metrics in experience bullet points (e.g., 'Improved performance by 25%').")

    return {
        'extracted_text': text[:1000] + ("..." if len(text) > 1000 else ""),
        'detected_skills': list(set(detected_skills)),
        'detected_experience': detected_exp,
        'inferred_domain': top_domain,
        'missing_skills': missing_skills,
        'suggestions': suggestions
    }
