import streamlit as st
st.set_page_config(page_title="SimuATS", layout="wide")

import time
import os
import torch
from modules.extract_skills import extract_skills_from_text
from modules.skill_ranker import rank_skills
from modules.resume_matcher import score_resume_against_skills
from modules.suggestions import suggest_rewordings
from io import StringIO
import docx2txt
import pdfplumber

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
if "resume_results" not in st.session_state:
    st.session_state.resume_results = None
if "revised_resume" not in st.session_state:
    st.session_state.revised_resume = None

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

        st.session_state.job_description = job_description_input.strip()

        extracted_skills = extract_skills_from_text(job_description_input)
        st.session_state.extracted_skills = extracted_skills

        if extracted_skills:
            inference_start = time.time()
            ranked = rank_skills(job_description_input, extracted_skills)
            st.session_state.ranked = ranked
            st.session_state.inference_time = time.time() - inference_start
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
        st.markdown(f"**{skill}** — Importance Score: **{score}**")

    if st.session_state.inference_time and st.session_state.total_time:
        st.markdown("### Performance")
        st.write(f"Inference runtime: **{st.session_state.inference_time:.2f} seconds**")
        st.write(f"Total processing time: **{st.session_state.total_time:.2f} seconds**")

    if torch and torch.cuda.is_available():
        st.write(f"Running on GPU: **{torch.cuda.get_device_name(0)}**")
    else:
        st.write("Running on CPU — GPU not available.")

    # --- RESUME INPUT & GPT SCORING ---

    def parse_uploaded_resume(uploaded_file):
        if uploaded_file.name.endswith(".pdf"):
            with pdfplumber.open(uploaded_file) as pdf:
                text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        elif uploaded_file.name.endswith(".docx"):
            text = docx2txt.process(uploaded_file)
        else:
            text = ""
        return text.strip()

    st.subheader("Upload or paste your resume for scoring:")

    uploaded_resume = st.file_uploader(
        "Upload PDF or DOCX resume", type=["pdf", "docx"]
    )

    resume_text_input = ""
    resume_filename = None

    if uploaded_resume is not None:
        resume_filename = uploaded_resume.name
        resume_text_input = parse_uploaded_resume(uploaded_resume)
        if resume_text_input:
            st.success("Resume extracted successfully.")
            st.info(f"Uploaded file: {resume_filename}")
        else:
            st.warning("Could not extract text from the uploaded file.")
    else:
        resume_text_input = st.session_state.resume_text

    resume_text_input = st.text_area(
        "Resume Text:",
        height=300,
        value=resume_text_input
    )

    # --- EVALUATE RESUME ---

    if st.button("Evaluate Resume"):
        if resume_text_input.strip():
            st.session_state.resume_text = resume_text_input.strip()
            resume_results = score_resume_against_skills(
                resume_text_input,
                st.session_state.job_description
            )
            st.session_state.resume_results = resume_results
        else:
            st.warning("Please provide resume text.")

    if st.session_state.resume_results:
        st.subheader(f"Resume Score: {st.session_state.resume_results['score']} / 100")
        st.write(st.session_state.resume_results['justification'])

    # --- SUGGEST IMPROVEMENTS ---

    if st.button("Suggest Improvements"):
        if resume_text_input.strip():
            with st.spinner("Generating improvement suggestions..."):
                revised_resume = suggest_rewordings(
                    resume_text_input.strip(),
                    st.session_state.job_description,
                    st.session_state.extracted_skills
                )
                st.session_state.revised_resume = revised_resume

            st.subheader("Your revised resume:")
            st.write(st.session_state.revised_resume)

        else:
            st.warning("Please provide resume text or upload a file.")

else:
    st.info("Submit a job description first to enable resume scoring.")
