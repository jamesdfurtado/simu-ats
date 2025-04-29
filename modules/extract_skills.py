import os
import re
import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
nltk.download('omw-1.4')

lemmatizer = WordNetLemmatizer()

skills_path = os.path.join(os.path.dirname(__file__), '../text/hard_skills.txt')
with open(skills_path, 'r', encoding='utf-8') as file:
    raw_skills = [line.strip().lower() for line in file if line.strip()]

normalized_skills = set()
for skill in raw_skills:
    skill_cleaned = re.sub(r'[^a-z0-9\s\+\#\.\-]', '', skill)
    skill_normalized = ' '.join([lemmatizer.lemmatize(word) for word in skill_cleaned.split()])
    normalized_skills.add(skill_normalized)

skill_collision_rules = {
    "es6": {"javascript", "js"}
}

def extract_skills_from_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s\+\#\.\-]', ' ', text)
    words = text.split()

    # Skip lemmatizing words with +, #, or . inside
    lemmatized_words = []
    for word in words:
        if '+' in word or '#' in word or '.' in word:
            lemmatized_words.append(word)
        else:
            lemmatized_words.append(lemmatizer.lemmatize(word))

    lemmatized_text = ' '.join(lemmatized_words)

    extracted = set()
    for skill in normalized_skills:
        pattern = r'(?<!\w)' + re.escape(skill) + r'(?!\w)'
        if re.search(pattern, lemmatized_text):
            extracted.add(skill)

    for weak_skill, strong_skills in skill_collision_rules.items():
        if weak_skill in extracted:
            if any(strong in extracted for strong in strong_skills):
                extracted.discard(weak_skill)

    # Special handling for Go language detection
    go_phrases = {
        "in go", "with go", "using go",
        "go language", "go development", "go code", "go programming", "go engineer",
        "go developer", "go stack", "go microservices", "go backend", "go application",
        "go based", "go tools", "go runtime", "golang"
    }

    if any(phrase in lemmatized_text for phrase in go_phrases):
        extracted -= go_phrases
        extracted.add("go")

    # Fix "cs" confusion if not meant to be css
    if "cs" in extracted and "css" not in extracted:
        extracted.remove("cs")
        extracted.add("css")
    
    if "panda" in extracted:
        extracted.remove("panda")
        extracted.add("pandas")

    if "c" in extracted and "c++" in extracted:
        extracted.remove("c")

    return sorted(extracted)

# This is before skill importance is ranked
