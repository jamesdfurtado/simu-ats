import streamlit as st

st.set_page_config(page_title="SimuATS", layout="wide")

# Title and subtitle at top-left
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
    else:
        st.warning("Enter a job description before submitting.")
