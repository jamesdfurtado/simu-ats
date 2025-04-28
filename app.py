import streamlit as st
from modules.job_parser import clean_and_chunk_text

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

        # Process the pasted job description
        chunks = clean_and_chunk_text(job_description)

        st.write(f"Total Chunks Created: {len(chunks)}")
        for idx, chunk in enumerate(chunks):
            st.write(f"**Chunk {idx+1}:** {chunk}")

    else:
        st.warning("Enter a job description before submitting.")
