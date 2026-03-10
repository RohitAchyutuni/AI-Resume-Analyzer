import streamlit as st
import tempfile
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from main2 import run_langchain_ats
# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Frontier AI Recruiter",
    page_icon="✈️",
    layout="wide"
)

# Frontier Airlines Brand Colors (Approximate)
# Green: #006644 | Silver/Grey: #A7A9AC
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { background-color: #006644; color: white; border-radius: 8px; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e1e4e8; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR INPUTS ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/b/b3/Frontier_Airlines_logo.svg", width=200)
    st.title("Settings")
    
    api_key = st.text_input("Groq API Key", type="password", help="Enter your gsk_... key, ")
    
    st.divider()


    st.subheader("➕ Add New Candidate")
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
    
    if uploaded_file and st.button("📥 Save to Database"):
        with st.spinner("Processing PDF..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name
            
            try:
                # Logic copied from your ingestion script
                loader = PyPDFLoader(tmp_path)
                docs = loader.load()
                splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
                chunks = splitter.split_documents(docs)
                
                # Tagging with filename
                for chunk in chunks:
                    chunk.metadata["candidate"] = uploaded_file.name
                
                # Saving to ChromaDB
                embeddings = OllamaEmbeddings(model="nomic-embed-text")
                db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
                db.add_documents(chunks)
                
                st.success(f"Added {uploaded_file.name} to DB!")
            finally:
                os.remove(tmp_path)
    
    st.divider()
    
    st.subheader("Target Role")
    jd_input = st.text_area(
        "Job Description", 
        height=350,
        placeholder="Paste the job description here...",
        value="""Role: Summer 2026 AI Assisted Developer Internship at Frontier Airlines
Requirements:
- Strong proficiency in Python.
- Experience with Generative AI, LLMs, and frameworks like LangChain or CrewAI.
- Familiarity with building and evaluating AI agents or RAG pipelines.
- Ability to write clean, maintainable code and integrate APIs."""
    )

# --- 3. MAIN DASHBOARD ---
st.title("✈️ AI Candidate Screening Dashboard")
st.info("This system analyzes candidates stored in your vector database against the job requirements using structured RAG pipelines.")

if st.button("🚀 Start Screening Process"):
    if not api_key or not jd_input:
        st.error("Please provide both the API Key and the Job Description in the sidebar.")
    else:
        # We use a status container to look more professional than just a spinner
        with st.status("Initializing AI Recruiter...", expanded=True) as status:
            st.write("Fetching candidates from database...")
            # CALL YOUR ENGINE
            results = run_langchain_ats(jd_input, api_key)
            
            if results:
                status.update(label="Screening Complete!", state="complete", expanded=False)
                st.balloons()
                
                # --- 4. DISPLAY RESULTS ---
                st.divider()
                
                # Winner Highlight
                winner = results[0]
                st.subheader(f"🏆 Top Candidate Match: {winner['candidate']}")
                
                # Top metrics
                m_col1, m_col2, m_col3 = st.columns(3)
                m_col1.metric("Top Score", f"{winner['score']}%")
                m_col2.metric("Candidates Screened", len(results))
                m_col3.metric("Status", "Selection Ready")

                st.write("---")

                # Detailed Leaderboard
                st.subheader("📋 Screening Results")
                
                for i, candidate in enumerate(results):
                    # Use an expander for each candidate
                    with st.expander(f"Rank #{i+1}: {candidate['candidate']} — Score: {candidate['score']}%"):
                        c_col1, c_col2 = st.columns([1, 2])
                        
                        with c_col1:
                            st.write("**Match Accuracy**")
                            # Color logic for the score
                            color = "green" if candidate['score'] > 75 else "orange" if candidate['score'] > 50 else "red"
                            st.markdown(f"### <span style='color:{color}'>{candidate['score']}%</span>", unsafe_allow_html=True)
                            st.progress(candidate['score'] / 100)
                            
                        with c_col2:
                            st.write("**Improvement Areas / Feedback:**")
                            for point in candidate['feedback']:
                                st.write(f"• {point}")
            else:
                status.update(label="No candidates found.", state="error")
                st.warning("Database is empty. Please run your ingestion script first.")

# --- 5. FOOTER ---
st.divider()
st.caption("Proprietary AI Screening Tool for internal use only.")