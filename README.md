# simu-ats
A simulated ATS resume scanner with AI evaluation and suggestions.

# SimuATS - ATS Resume Optimizer

## 1. Name of Project Partner
Solo Project – James Furtado

## 2. Title of the Project
AI-Powered ATS Resume Optimizer

## 3. Clear Description of the Project
SimuATS is a web-based tool that helps job applicants tailor their resumes to specific job postings using AI. Users will upload a job description, and the AI will create its best representation of what the company’s ATS might look like. After this, the user can pass in a resume(s). The AI will then analyze the match and provide a score of 0-100. Then, it will give feedback on keyword alignment, formatting, and overall content fit. It also will have the option to generate a sample "ideal" resume based on the job description, which will give the user an idea of how to tweak their own.

### Core Features
- Simple Web Interface
- Simulated ATS Machine Creation by copy-pasting a job description
- AI Resume Evaluation and feedback (0-100 score, keywords, formatting, wording)
- “Ideal” Resume Generator

This project is worth doing because it targets a real frustration in the job application process—getting past automated resume screeners (ATS). It gives users immediate, targeted feedback and helps them improve their applications with confidence and clarity.

## 4. Resources to Use
- **Local LLMs via Ollama** – Small, open-source models like phi, mistral, or llama3 will be used to generate resume content and provide AI-based feedback. These models run entirely on the local machine, avoiding API usage fees.
- **Embeddings & Retrieval** – The sentence-transformers library (e.g., all-MiniLM-L6-v2) will be used to embed both job descriptions and resume content. FAISS will be used to efficiently compare and retrieve the most relevant matches.
- **Labs** – Prompt Engineering, Assistants and Tools, Retrieval + File Uploads

### Tech Stack
- **Frontend**: Streamlit
- **Backend API**: FastAPI
- **Model Server**: Ollama locally → maybe API later
- **Deployment**: We’ll pick later.

## 5. Deliverables
- A working web application where users can upload job descriptions and resumes, receive feedback, and generate optimized sample resumes.
- GitHub repository with complete codebase and documentation
- Testing and evaluation of AI-generated resume suggestions

### Project Timeline
- April 24: Proposal submission
- April 26: Text-based input and scoring MVP
- April 29: Resume generation & UI feedback components
- May 2: Integration polish + file upload handling
- May 5: Project demo and final submission


van der Goot, Rob, Üstün, Ahmet, Ramponi, Alan, Sharaf, Ibrahim, and Plank, Barbara.  
*Massive Choice, Ample Tasks (MaChAmp): A Toolkit for Multi-task Learning in NLP.*  
Proceedings of the 16th Conference of the European Chapter of the Association for Computational Linguistics: System Demonstrations, 2021.  
[https://aclanthology.org/2021.eacl-demos.22](https://aclanthology.org/2021.eacl-demos.22)

