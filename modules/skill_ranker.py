import nltk
import streamlit as st
from transformers import pipeline
from typing import List, Dict, Union

# Download NLTK tokenizer if not present
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

# Load the zero-shot classification pipeline with BART MNLI
@st.cache_resource
def load_classifier():
    return pipeline(
        "zero-shot-classification",
        model="facebook/bart-large-mnli",
        device=0  # GPU
    )

_classifier = load_classifier()

# Optimized hypotheses
CANDIDATE_LABELS = [
    "This skill is essential and critical for the job.",
    "This skill is important but not strictly required.",
    "This skill is optional or nice-to-have."
]

LABEL_TO_SCORE = {
    "This skill is essential and critical for the job.": 3,
    "This skill is important but not strictly required.": 2,
    "This skill is optional or nice-to-have.": 1
}

def rank_skills(
    job_text: str,
    extracted_skills: List[str]
) -> Dict[str, Dict[str, Union[int, float, str]]]:

    job_text = job_text.lower()
    sentences = nltk.sent_tokenize(job_text)

    ranked_skills = {}

    for skill in extracted_skills:
        # Find sentences mentioning the skill
        relevant_text = " ".join(s for s in sentences if skill.lower() in s)
        if not relevant_text:
            relevant_text = job_text  # fallback to full job description

        # Run zero-shot classification comparing to all three hypotheses
        result = _classifier(
            relevant_text,
            candidate_labels=CANDIDATE_LABELS,
            multi_label=False
        )

        top_label = result['labels'][0]
        score = LABEL_TO_SCORE.get(top_label, 1)
        entailment_confidence = round(result['scores'][0], 3)

        ranked_skills[skill] = {
            "score": score,
            "top_label": top_label,
            "entailment_confidence": entailment_confidence,
            "relevant_text": relevant_text
        }

    return ranked_skills
