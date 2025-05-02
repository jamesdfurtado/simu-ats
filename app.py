import streamlit as st
st.set_page_config(page_title="SimuATS", layout="wide")

import time
import torch
from modules.extract_skills import extract_skills_from_text
from modules.skill_ranker import rank_skills

st.markdown("# SimuATS")
st.markdown("A simulated ATS resume scanner with AI evaluation and suggestions.")
st.write("")

st.write("Paste the job description below:")
job_description = st.text_area("", height=300, label_visibility="collapsed")

if st.button("Submit"):
    if job_description.strip():
        total_start = time.time()
        st.success("Job description received.")

        extracted_skills = extract_skills_from_text(job_description)

        if extracted_skills:
            st.subheader("Extracted Hard Skills:")
            st.write(", ".join(extracted_skills))

            inference_start = time.time()
            ranked = rank_skills(job_description, extracted_skills)
            inference_duration = time.time() - inference_start

            st.subheader("AI-Based Skill Importance:")

            for skill, info in ranked.items():
                score = info['score']
                entailment = info['entailment_confidence']
                relevant_text = info['relevant_text'] or "(No matching sentence found)"

                st.markdown(f"**{skill}**")
                st.write(f"- Importance Score: {score}")
                st.write(f"- Entailment Score: {entailment}")
                st.write(f"- Relevant Text: \"{relevant_text}\"")
                st.markdown("---")

            total_duration = time.time() - total_start

            st.markdown("### Performance")
            st.write(f"⏱️ Inference runtime: **{inference_duration:.2f} seconds**")
            st.write(f"🕒 Total processing time: **{total_duration:.2f} seconds**")

            if torch and torch.cuda.is_available():
                st.write(f"✅ Running on GPU: **{torch.cuda.get_device_name(0)}**")
            else:
                st.write("⚠️ Running on CPU — GPU not available.")
        else:
            st.info("No hard skills matched.")
    else:
        st.warning("Enter a job description before submitting.")
