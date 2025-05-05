import streamlit as st
st.set_page_config(page_title="SimuATS", layout="wide")

import time
import os
import torch
from modules.extract_skills import extract_skills_from_text
from modules.skill_ranker import rank_skills
from modules.resume_matcher import score_resume_against_skills

# --- LOAD DEFAULT FILES ---
def load_default_text(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    return ""

default_job_text = load_default_text("text/job.txt")
default_resume_text = load_default_text("text/resume.txt")

# --- SESSION STATE INITIALIZATION ---
if "ranked" not in st.session_state:
    st.session_state.ranked = None
if "extracted_skills" not in st.session_state:
    st.session_state.extracted_skills = []
if "job_description" not in st.session_state:
    st.session_state.job_description = default_job_text
if "resume_text" not in st.session_state:
    st.session_state.resume_text = default_resume_text

st.markdown("# SimuATS")
st.markdown("A simulated ATS resume scanner with AI evaluation and suggestions.")
st.markdown("Please do not include junk text (UI buttons and other text not related to the JD).")
st.write("")

# --- JOB DESCRIPTION INPUT ---
st.write("Paste the job description below:")

job_description_input = st.text_area(
    "",
    height=300,
    label_visibility="collapsed",
    value=st.session_state.job_description
)

if st.button("Submit"):
    if job_description_input.strip():
        total_start = time.time()
        st.success("Job description received.")

        # Save job description to session_state
        st.session_state.job_description = job_description_input.strip()

        extracted_skills = extract_skills_from_text(job_description_input)
        st.session_state.extracted_skills = extracted_skills

        if extracted_skills:
            inference_start = time.time()
            ranked = rank_skills(job_description_input, extracted_skills)
            st.session_state.ranked = ranked
            inference_duration = time.time() - inference_start

            st.session_state.inference_time = inference_duration
            st.session_state.total_time = time.time() - total_start

        else:
            st.session_state.ranked = None
            st.session_state.inference_time = None
            st.session_state.total_time = None

    else:
        st.warning("Enter a job description before submitting.")

# --- ALWAYS DISPLAY PREVIOUS RESULTS IF AVAILABLE ---

if st.session_state.extracted_skills:
    st.subheader("Extracted Hard Skills:")
    st.write(", ".join(st.session_state.extracted_skills))

if st.session_state.ranked:
    st.subheader("AI-Based Skill Importance:")

    for skill, info in st.session_state.ranked.items():
        score = info['score']
        entailment = info['entailment_confidence']
        relevant_text = info['relevant_text'] or "(No matching sentence found)"

        st.markdown(f"**{skill}**")
        st.write(f"- Importance Score: {score}")
        st.write(f"- Entailment Score: {entailment}")
        st.write(f"- Premise: \"{info['premise']}\"")
        st.write(f"- Hypothesis: \"{info['hypothesis']}\"")
        st.markdown("---")

    if st.session_state.inference_time and st.session_state.total_time:
        st.markdown("### Performance")
        st.write(f"⏱️ Inference runtime: **{st.session_state.inference_time:.2f} seconds**")
        st.write(f"🕒 Total processing time: **{st.session_state.total_time:.2f} seconds**")

    if torch and torch.cuda.is_available():
        st.write(f"✅ Running on GPU: **{torch.cuda.get_device_name(0)}**")
    else:
        st.write("⚠️ Running on CPU — GPU not available.")

# --- RESUME INPUT & GPT SCORING ---

if st.session_state.ranked:
    st.subheader("Paste your resume below for scoring:")

    resume_text_input = st.text_area(
        "Your resume:",
        height=300,
        value=st.session_state.resume_text
    )

    if st.button("Evaluate Resume"):
        if resume_text_input.strip():
            # Save resume to session_state so it stays
            st.session_state.resume_text = resume_text_input.strip()

            resume_results = score_resume_against_skills(
                resume_text_input,
                st.session_state.job_description
            )

            st.subheader(f"Resume Score: {resume_results['score']} / 100")
            st.write(resume_results['justification'])

        else:
            st.warning("Please paste your resume before evaluating.")
else:
    st.info("Submit a job description first to enable resume scoring.")
