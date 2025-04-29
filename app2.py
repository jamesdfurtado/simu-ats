import streamlit as st
from modules.extract_skills import extract_skills_from_text
from modules.skill_ranker import rank_skills  # ✅ new import

st.set_page_config(page_title="SimuATS", layout="wide")

st.markdown("# SimuATS")
st.markdown("A simulated ATS resume scanner with AI evaluation and suggestions.")
st.write("")

st.write("Paste the job description below:")
job_description = st.text_area("", height=300)

if st.button("Submit"):
    if job_description.strip():
        st.success("Job description received.")

        # Extract hard skills
        extracted_skills = extract_skills_from_text(job_description)

        if extracted_skills:
            st.subheader("Extracted Hard Skills:")
            st.write(", ".join(extracted_skills))

            # ✅ Rank skills using AI
            ranked = rank_skills(job_description, extracted_skills)

            st.subheader("AI-Based Skill Importance:")
            for skill, score in ranked.items():
                st.write(f"**{skill}** — Importance Score: {score}")
        else:
            st.info("No hard skills matched.")
    else:
        st.warning("Enter a job description before submitting.")
