import openai
import io
from docx import Document
from PyPDF2 import PdfReader, PdfWriter

def suggest_rewordings(resume_text, job_description, extracted_skills):
    system_prompt = (
        "You are an experienced technical resume reviewer. "
        "Your only task is to suggest rewordings or improvements to the user's resume text "
        "to better align with the provided job description and extracted skills. "
        "You must strictly retain the user's original writing style and NEVER introduce or fabricate skills, experiences, or tools that are not already present. "
        "If sections do not need improvement, leave them unchanged. "
        "Your output should be a fully rewritten resume in plain text format, preserving the original structure."
    )

    user_prompt = (
        f"Job Description:\n{job_description}\n\n"
        f"Extracted Skills:\n{', '.join(extracted_skills)}\n\n"
        f"Resume Text:\n{resume_text}\n\n"
        "Please rewrite the resume where appropriate to better match the job description. Retain writing style and only reword existing content."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2
    )

    suggestions = response["choices"][0]["message"]["content"]
    return suggestions

def apply_rewordings_to_file(uploaded_file, new_text):
    if uploaded_file.name.endswith(".docx"):
        doc = Document()
        for para in new_text.strip().split("\n\n"):
            doc.add_paragraph(para.strip())
        bio = io.BytesIO()
        doc.save(bio)
        bio.seek(0)
        return {
            "data": bio,
            "filename": "revised_resume.docx",
            "mime": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        }

    elif uploaded_file.name.endswith(".pdf"):
        # Simple text-based PDF creation (preserves text but not styling)
        from fpdf import FPDF

        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)

        for line in new_text.split("\n"):
            pdf.multi_cell(0, 10, line)

        bio = io.BytesIO()
        pdf.output(bio)
        bio.seek(0)

        return {
            "data": bio,
            "filename": "revised_resume.pdf",
            "mime": "application/pdf"
        }

    else:
        return None
