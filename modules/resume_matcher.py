import openai
import os
from dotenv import load_dotenv

# Load OpenAI key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def score_resume_against_skills(resume_text: str, job_description: str) -> dict:
    """
    Uses GPT to score how well the resume matches the job description.
    Returns a score out of 100 and a justification.
    """

    system_prompt = (
        "You are an applicant tracking system (ATS) evaluation assistant. "
        "Given a job description and a resume, you will assess how well the resume matches the job description. "
        "Your output should be a score from 1 to 100 (with 100 meaning a perfect fit) and a short explanation of why."
    )

    user_prompt = (
        f"Job Description:\n{job_description}\n\n"
        f"Resume:\n{resume_text}\n\n"
        "Please provide only the score (as a number from 1 to 100), followed by a one-sentence justification."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # or "gpt-4o" if you want to save tokens
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0
        )

        reply = response.choices[0].message.content.strip()

        # Attempt to parse the score and justification
        lines = reply.split("\n")
        score = None
        justification = ""

        for line in lines:
            if any(char.isdigit() for char in line):
                possible_score = ''.join(filter(str.isdigit, line))
                if possible_score:
                    score = int(possible_score)
                    justification = line
                    break

        if score is None:
            score = 0
            justification = "Could not parse score."

        return {
            "score": min(max(score, 0), 100),  # clamp between 0 and 100
            "justification": justification
        }

    except Exception as e:
        return {
            "score": 0,
            "justification": f"Error during evaluation: {str(e)}"
        }
