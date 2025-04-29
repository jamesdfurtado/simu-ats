import nltk
from transformers import pipeline
from typing import List, Dict, Union

nltk.download('punkt')

# Initialize zero-shot classifier (can be reused for multiple calls)
_classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
    device=-1  # use CPU; change to 0 if using GPU
)

# Define scoring labels and mapping
CANDIDATE_LABELS = [
    "critical requirement",
    "important but not critical",
    "relevant but optional",
    "barely mentioned"
]

LABEL_TO_SCORE = {
    "critical requirement": 4,
    "important but not critical": 3,
    "relevant but optional": 2,
    "barely mentioned": 1
}

def rank_skills(
    job_text: str,
    extracted_skills: List[str],
    show_confidence: bool = False
) -> Union[Dict[str, int], Dict[str, Dict[str, Union[int, float]]]]:
    """
    Rank each skill on a 1–4 scale using zero-shot classification.
    Returns {skill: score}, or if show_confidence=True,
    {skill: {'score': score, 'confidence': float}}
    """
    job_text = job_text.lower()
    sentences = nltk.sent_tokenize(job_text)

    ranked_skills = {}

    for skill in extracted_skills:
        # Gather only relevant sentences for each skill
        relevant_text = " ".join(s for s in sentences if skill in s.lower())

        if not relevant_text:
            relevant_text = job_text  # fallback to full text

        result = _classifier(
            relevant_text,
            candidate_labels=CANDIDATE_LABELS,
            multi_label=False
        )

        top_label = result['labels'][0]
        score = LABEL_TO_SCORE.get(top_label, 1)

        if show_confidence:
            ranked_skills[skill] = {
                "score": score,
                "confidence": round(result['scores'][0], 3)
            }
        else:
            ranked_skills[skill] = score

    return ranked_skills
