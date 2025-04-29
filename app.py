import streamlit as st
from modules.extract_skills import extract_skills_from_text

st.set_page_config(page_title="SimuATS", layout="wide")

# Title and subtitle
st.markdown("# SimuATS")
st.markdown("A simulated ATS resume scanner with AI evaluation and suggestions.")

st.write("")

# Job description input
st.write("Paste the job description below:")
job_description = st.text_area("", height=300)

# Submit button
if st.button("Submit"):
    if job_description.strip():
        st.success("Job description received.")

        # Extract hard skills
        extracted_skills = extract_skills_from_text(job_description)

        if extracted_skills:
            st.subheader("Extracted Hard Skills:")
            st.write(", ".join(extracted_skills))
        else:
            st.info("No hard skills matched.")
    else:
        st.warning("Enter a job description before submitting.")