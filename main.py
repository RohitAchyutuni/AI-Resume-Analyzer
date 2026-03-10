# import os 
# from crewai import Agent, Task, Crew, Process, LLM
# from crewai.tools import tool
# from langchain_ollama import OllamaEmbeddings
# from langchain_community.vectorstores import Chroma

# # Define the agent's task
# os.environ["GROQ_API_KEY"] = ""
# llama_llm = LLM(model="groq/llama-3.1-8b-instant", temperature=0)

# @tool("List Candidates Tool")
# def list_candidates_tool(dummy_arg:str) -> str:
#     """Return a list of all unique candidate filenames currently in the database.
#     You can ppass check on any string or argument 
#     """
#     print("\n [TOOL TRIGGERED] Checking db for candidates")
#     db = Chroma(persist_directory="./chroma_db", embedding_function=OllamaEmbeddings(model="nomic-embed-text"))

#     try:
#         metadatas = db.get()['metadatas']
#         if not metadatas:
#             return "No candidates found in the database."
#         candidates = list(set([m['candidate'] for m in metadatas if 'candidate' in m]))
#         return f"Candidates in database: {', '.join(candidates)}"
#     except Exception as e:
#         print(f"\n [ERROR] Failed to retrieve candidates: {e}")
#         return "An error occurred while checking the database."
    
# @tool("Candidate Info Tool")
# def targeted_search_tool(search_query:str, candidate_name:str) -> str:
#     """Search for specific information about a candidate in the database.
#     'candidate_name' MUST be the exact filename returned by the List Candidates Tool."""
#     print(f"\n [TOOL TRIGGERED] Searching for '{search_query}' in {candidate_name}'s data")
#     db = Chroma(persist_directory="./chroma_db", embedding_function=OllamaEmbeddings(model="nomic-embed-text"))
    
#     results = db.similarity_search(
#         search_query, 
#         k=4, 
#         filter={"candidate": candidate_name} 
#     )
    
#     if not results:
#         return f"No information found for {candidate_name} regarding '{search_query}'."
        
#     return "\n\n---\n\n".join([doc.page_content for doc in results])
    

# job_description = """
# Role: Summer 2026 AI Assisted Developer Internship at Frontier Airlines
# Requirements:
# - Strong proficiency in Python.
# - Experience with Generative AI, LLMs, and frameworks like LangChain or CrewAI.
# - Familiarity with building and evaluating AI agents or RAG pipelines.
# - Ability to write clean, maintainable code and integrate APIs.
# """

# recruiter = Agent(
#     name="Candidate Screening Agent",
#     role="Screen candidates for the Summer 2026 AI Assisted Developer Internship at Frontier Airlines",
#     goal="Identify and evaluate top candidates based on their qualifications and fit for the internship role",
#     backstory="You are an experienced HR professional with a keen eye for identifying talented developers who can contribute to Frontier Airlines' AI initiatives.",
#     verbose=True,
#     llm=llama_llm, 
#     tools=[list_candidates_tool, targeted_search_tool],
#     allow_delegation=False
# )

# # Define the task for the agent
# review_task = Task(
#     description=f'''
# You are evaluating candidates for the following role: 
# {job_description}

# CRTICAL STEPS FOR SYSTEM OVERRIDE:
# 1. Use the "List Candidates Tool" to get an overview of all candidates currently in the database.
# 2. For each candidate, use the "Candidate Info Tool" to search for specific qualifications,
#     experiences, or projects that demonstrate their fit for the role.
# 3. For each candidate filenamefound in step 1, you  must trigger the "targeted_search_tool
# 4. Wait to receive the raw text chunks for each candidate 
# 5. Evaluate each candidate's qualifications based on the retrieved information and compare it against the job requirements.''',
# expected_output=''' You MUST output a final report ONLY IF THE MATCH SCORE IS ABOVE 75 and formatted exactly like this for EVERY candidate:
    
#     --- CANDIDATE: [Filename] ---
#     1. DATABASE EVIDENCE: (Provide the exact, raw quotes you pulled).
#     2. MATCH SCORE: (Score from 0-100 based ONLY on the evidence).
#     3. FEEDBACK: (3 actionable bullet points of what they are missing or should emphasize).
#     ''',
#     agent=recruiter
# )

# # Create a crew and add the task
# resume_crew = Crew(
#     agents=[recruiter],
#     tasks=[review_task],
#     process=Process.sequential
# )

# if __name__ == "__main__":
#     print("Starting Multi-Candidate ATS Evaluation...\n")
#     result = resume_crew.kickoff()
#     print("\n================ FINAL REPORT ================\n")
#     print(result)