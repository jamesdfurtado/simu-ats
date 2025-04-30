import nltk
import os
import time
import streamlit as st
from transformers import pipeline
from typing import List, Dict, Union

# Only import torch if running as script to avoid unnecessary load in Streamlit
try:
    import torch
except ImportError:
    torch = None

# Download tokenizer if not already present
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

# Determine if we're running inside Streamlit
RUNNING_IN_STREAMLIT = os.getenv("RUNNING_IN_STREAMLIT", "0") == "1"

# Load model with or without caching
if RUNNING_IN_STREAMLIT:
    @st.cache_resource
    def load_classifier():
        return pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli",
            device=0  # ✅ Use GPU
        )
    _classifier = load_classifier()
else:
    _classifier = pipeline(
        "zero-shot-classification",
        model="facebook/bart-large-mnli",
        device=0  # ✅ Use GPU
    )

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
    """
    Rank each skill on a 1–4 scale using zero-shot classification.
    Returns {skill: score}, or if show_confidence=True,
    {skill: {'score': score, 'confidence': float}}
    """
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

# Standalone test mode
if __name__ == "__main__":
    start_time = time.time()

    job_description = """
    The Software Engineer Associate will work on applications using Python, C++, OpenCV, and data pipelines.
    Experience with Agile development, computer vision, and APIs is important. Familiarity with Arduino is helpful.
    """

    extracted_skills = [
        "python", "c++", "opencv", "data pipeline",
        "agile", "computer vision", "apis", "arduino"
    ]

    # Report GPU status
    if torch:
        print(f"CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"Using GPU: {torch.cuda.get_device_name(0)}")
        else:
            print("⚠️  Not using GPU — falling back to CPU.")

    # Run scoring
    ranked = rank_skills(job_description, extracted_skills, show_confidence=True)

    from pprint import pprint
    pprint(ranked)

    duration = time.time() - start_time
    print(f"\n⏱️ Total runtime: {duration:.2f} seconds")
