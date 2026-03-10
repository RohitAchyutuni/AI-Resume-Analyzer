import os
from pydantic import BaseModel, Field
from typing import List
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

class CandidateEvaluation(BaseModel):
    score: int = Field(description="A number from 0 to 100 representing the match score based ONLY on the evidence.")
    feedback: List[str] = Field(description="Exactly 3 actionable bullet points of what they are missing or should emphasize.")
    candidate_name: str = Field(description="The exact name of the candidate being evaluated.")

os.environ["GROQ_API_KEY"] = ""
def run_langchain_ats(job_description, api_key):
    os.environ["GROQ_API_KEY"] = api_key
    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
    structured_evaluator_llm = llm.with_structured_output(CandidateEvaluation)
    emdeddings = OllamaEmbeddings(model="nomic-embed-text")
    db = Chroma(persist_directory="./chroma_db", embedding_function=emdeddings)

    job_description = """
Role: Summer 2026 AI Assisted Developer Internship at Frontier Airlines
    Requirements:
    - Strong proficiency in Python.
    - Experience with Generative AI, LLMs, and frameworks like LangChain or CrewAI.
    - Familiarity with building and evaluating AI agents or RAG pipelines.
    - Ability to write clean, maintainable code and integrate APIs.
    """

    print("checking db for candidates")
    if db.get()['metadatas']:
        candidates = list(set([m['candidate'] for m in db.get()['metadatas'] if 'candidate' in m]))
        print(f"Candidates in database: {', '.join(candidates)}")
    else:
        print("No candidates found in the database.")

    search_prompt = ChatPromptTemplate.from_template("Based on the job description: {job_description}, extract the core technical skills into one sentence.")

    search_chain = search_prompt | llm | StrOutputParser()

    eval_propmt = ChatPromptTemplate.from_template('''
 You are a strict Senior AI Technical Recruiter. Evaluate this candidate based ONLY on the provided database evidence.
    Do not hallucinate skills. If it's not in the evidence, they don't have it.
    
    Job Description: {jd}
    Candidate Database Evidence: 
    {evidence}
    
    Output exactly:
        PRINT ONLY THE TOP "1" CANDIDATE NAME, MATCH SCORE, AND FEEDBACK IN THIS EXACT FORMAT:
    --- CANDIDATE: {candidate_name} ---
    1. MATCH SCORE: (Score from 0-100 based strictly on the evidence matching the JD)
    2. FEEDBACK: (3 highly actionable bullet points of what they are missing or should emphasize)
    ''')

    eval_chain = eval_propmt | structured_evaluator_llm

    print("Generate search query ")
    search_query = search_chain.invoke({"job_description": job_description})
    print(f"\n[SEARCH QUERY]: {search_query}")

    print("\nEvaluating candidates based on database evidence...")
    all_evaluations = []
    for candidate in candidates:
        print(f"\n--- Evaluating {candidate} ---")
        results = db.similarity_search(search_query, k=4, filter={"candidate": candidate})
        evidence = "\n\n---\n\n".join([doc.page_content for doc in results])
        
        evaluation = eval_chain.invoke({
            "jd": job_description,
            "evidence": evidence,
            "candidate_name": candidate
        })

        all_evaluations.append(
            {
                "candidate": candidate,
                "score": evaluation.score,
                "feedback": evaluation.feedback
            }
        )
        
        print(evaluation)

    all_evaluations.sort(key=lambda x: x["score"], reverse=True)
    return all_evaluations


