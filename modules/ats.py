# modules/ats.py

from gradio_client import Client

# Blocklist of known soft skills, noise, and vague terms
NOISE_TERMS = {
    "bachelor’s degree", "computer science", "engineering", "learning",
    "application stack", "cloud", "modern", "collaboration",
    "communication", "leadership", "teamwork", "problem solving",
    "adaptability", "creativity", "motivation", "attention to detail",
    "organization", "interpersonal skills", "time management"
}

def extract_skills_from_chunks(chunks):
    """
    Given a list of text chunks, runs skill extraction and returns a clean, deduplicated list:
    - hard_skills (only)
    """
    client = Client("jjzha/skill_extraction_demo")

    all_hard_skills = []

    for idx, chunk in enumerate(chunks):
        try:
            result = client.predict(
                text=chunk,
                api_name="/predict"
            )

            # Only extract hard skills (from the model's "Knowledge" category)
            hard_skills_raw = result[1]

            hard_skills = [item['token'] for item in hard_skills_raw if item['class_or_confidence'] == 'Knowledge']

            all_hard_skills.extend(hard_skills)

        except Exception as e:
            print(f"Error processing chunk {idx+1}: {e}")

    # Post-process hard skills
    cleaned_hard_skills = clean_extracted_skills(all_hard_skills)

    return cleaned_hard_skills

def clean_extracted_skills(skills):
    """
    Cleans a list of extracted hard skills:
    - Splits combos like 'Python/Django' into ['Python', 'Django']
    - Removes noise terms
    - Deduplicates
    - Sorts alphabetically
    """
    cleaned_skills = []

    for skill in skills:
        skill = skill.strip().lstrip('/').rstrip('/')
        parts = skill.split('/')
        for part in parts:
            part_clean = part.strip().lower()
            if part_clean and part_clean not in NOISE_TERMS:
                cleaned_skills.append(part_clean)

    cleaned_skills = sorted(list(set(cleaned_skills)))

    return cleaned_skills
