# ✈️ Frontier AI Resume Recruiter
An automated Applicant Tracking System (ATS) built with **LangChain**, **ChromaDB**, and **Groq**. 

## 🚀 Features
- **RAG-Powered Evaluation:** Uses Vector Search to find specific technical evidence in resumes.
- **Type-Safe Grading:** Utilizes Pydantic Structured Outputs for consistent scoring.
- **Multi-Candidate Leaderboard:** Ranks multiple applicants based on Job Description fit.
- **Streamlit UI:** A professional dashboard for uploading resumes and viewing rankings.

## 🛠️ Tech Stack
- **LLM:** Llama 3.1 (via Groq)
- **Embeddings:** Nomic-Embed-Text (via Ollama)
- **Orchestration:** LangChain (LCEL)
- **Database:** ChromaDB

## 📦 Installation
1. Clone the repo: `git clone <your-repo-url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`