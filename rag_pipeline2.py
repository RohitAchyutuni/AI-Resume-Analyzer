import os
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def process_resumes_directory(directory_path):
    all_chunks = []
    
    # 1. Loop through every file in the folder
    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory_path, filename)
            print(f"Processing {file_path}...")
            
            # 2. Load the PDF document
            loader = PyPDFLoader(file_path)
            pages = loader.load()
            
            # 3. Attach the "Sticky Note" (Metadata)
            for page in pages:
                page.metadata["candidate"] = filename  
            
            # 4. Turn on the text splitter and chop the pages
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = text_splitter.split_documents(pages)
            
            all_chunks.extend(chunks)
            print(f"Extracted {len(chunks)} chunks from {filename}.")
            
    return all_chunks

def create_vector_store(chunks):
    print("\nCreating vector store...")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    persist_directory = "./chroma_db"
    
    # 5. Build and save the database
    vector_db = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings, 
        persist_directory=persist_directory
    )
    return vector_db

if __name__ == "__main__":
    resume_folder = "./resumes"
    
    # Check if the folder exists
    if not os.path.exists(resume_folder):
        os.makedirs(resume_folder)
        print(f"Created directory '{resume_folder}'. Please drop some PDFs inside and run again.")
    else:
        # Process all PDFs and tag them
        chunks = process_resumes_directory(resume_folder)
        
        if chunks:
            # Build the new multi-candidate database
            my_db = create_vector_store(chunks)
            print(f"\n✅ Total chunks across all candidates saved to database: {len(chunks)}")
        else:
            print("No PDFs found in the resumes folder. Please add some and try again!")