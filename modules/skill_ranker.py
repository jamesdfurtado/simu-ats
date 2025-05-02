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

# Base candidate labels with placeholder
CANDIDATE_LABELS_TEMPLATE = [
    "Experience with {skill} is essential and required.",
    "Experience with {skill} is preferred but not required.",
    "Experience with {skill} is optional, but not required."
]

LABEL_TO_SCORE = {
    "essential": 3,
    "preferred": 2,
    "optional": 1
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

        # Premise with context
        premise = f"This sentence is from a job description: {relevant_text}"

        # Dynamically create hypotheses for this skill
        candidate_labels = [
            label.format(skill=skill) for label in CANDIDATE_LABELS_TEMPLATE
        ]

        # Run zero-shot classification
        result = _classifier(
            premise,
            candidate_labels=candidate_labels,
            multi_label=False
        )

        top_label = result['labels'][0]
        entailment_score = round(result['scores'][0], 3)

        # Determine the score based on which label won
        if "essential" in top_label:
            importance = 3
        elif "preferred" in top_label:
            importance = 2
        else:
            importance = 1

        ranked_skills[skill] = {
            "score": importance,
            "entailment_confidence": entailment_score,
            "relevant_text": relevant_text,
            "premise": premise,
            "hypothesis": top_label
        }

    return ranked_skills




# Need to implement better parsing -- we need to know titles and make sure they aren't in our premise.
# We also need to implement header detection and put them IN our premises.


# For now, this doesn't work too too well. However, for the sake of handing in our project -- this will have to do for now.