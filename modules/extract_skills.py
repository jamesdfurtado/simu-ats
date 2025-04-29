import os
import re
import nltk
from nltk.stem import WordNetLemmatizer

# Download required resources if not already present
nltk.download('wordnet')
nltk.download('omw-1.4')

lemmatizer = WordNetLemmatizer()

# Load and normalize the hard skills list
skills_path = os.path.join(os.path.dirname(__file__), '../text/hard_skills.txt')
with open(skills_path, 'r', encoding='utf-8') as file:
    raw_skills = [line.strip().lower() for line in file if line.strip()]

# Normalize the hard skills list
normalized_skills = set()
for skill in raw_skills:
    skill_cleaned = re.sub(r'[^a-z0-9\s\+\#\.\-]', '', skill)  # Keep +, #, . for C++, Node.js, etc.
    skill_normalized = ' '.join([lemmatizer.lemmatize(word) for word in skill_cleaned.split()])
    normalized_skills.add(skill_normalized)

# Special collision rules (optional, for edge cases like JS/ES6)
skill_collision_rules = {
    "es6": {"javascript", "js"}
}

def extract_skills_from_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s\+\#\.\-]', ' ', text)  # Keep +, #, . for tech names
    words = text.split()
    lemmatized_text = ' '.join([lemmatizer.lemmatize(word) for word in words])

    extracted = set()
    for skill in normalized_skills:
        pattern = r'(?<!\w)' + re.escape(skill) + r'(?!\w)'
        if re.search(pattern, lemmatized_text):
            extracted.add(skill)

    # Apply collision rules (e.g., remove 'es6' if 'javascript' or 'js' is found)
    for weak_skill, strong_skills in skill_collision_rules.items():
        if weak_skill in extracted:
            if any(strong in extracted for strong in strong_skills):
                extracted.discard(weak_skill)

    # Handle "go" disambiguation
    go_phrases = {
        "in go", "with go", "using go",
        "go language", "go development", "go code", "go programming", "go engineer",
        "go developer", "go stack", "go microservices", "go backend", "go application",
        "go based", "go tools", "go runtime", "golang"
    }

    if any(phrase in lemmatized_text for phrase in go_phrases):
        extracted -= go_phrases
        extracted.add("golang")

    return sorted(extracted)
