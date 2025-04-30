import nltk
import streamlit as st
from transformers import pipeline
from typing import List, Dict, Union

# Download tokenizer if not already present
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

# Load and cache the model (GPU only)
@st.cache_resource
def load_classifier():
    return pipeline(
        "zero-shot-classification",
        model="facebook/bart-large-mnli",
        device=0  # ✅ Always use GPU
    )

_classifier = load_classifier()

# Scoring rubric
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
    job_text = job_text.lower()
    sentences = nltk.sent_tokenize(job_text)

    ranked_skills = {}

    for skill in extracted_skills:
        relevant_text = " ".join(s for s in sentences if skill in s.lower())
        if not relevant_text:
            relevant_text = job_text  # fallback if no specific mention

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