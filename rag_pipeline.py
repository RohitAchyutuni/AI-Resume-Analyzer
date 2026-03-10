# from langchain_community.document_loaders import PyPDFLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_ollama import OllamaEmbeddings # <-- The new Ferrari engine
# from langchain_community.vectorstores import Chroma

# def load_document(file_path):
#     loader = PyPDFLoader(file_path)
#     pages = loader.load()
#     print(f"Loaded {len(pages)} pages from {file_path}")
#     return pages

# def split_document(pages):
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#     chunks = text_splitter.split_documents(pages)
#     print(f"Split document into {len(chunks)} chunks.")
#     return chunks

# def create_vector_db(chunks):
#     print("Creating vector database...")
#     embeddings = OllamaEmbeddings(model="nomic-embed-text")
#     persist_directory = "./chroma_db"
#     vector_db = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=persist_directory)
#     print("Vector database created.")
#     return vector_db

# def retrieve_info(query, vector_db):
#     print(f"Retrieving information for query: {query}")
#     results = vector_db.similarity_search(query, k=2)
#     print(results[0].page_content)
#     return results

# if __name__ == "__main__":
#     file_path = "Rohit_Resume.pdf"  # Replace with your PDF file path
#     documents = load_document(file_path)
#     chunks = split_document(documents)
#     my_db = create_vector_db(chunks)
#     search_query = "Experience building RAG pipelines, LangChain, or evaluating LLMs"
#     top_matches = retrieve_info(search_query, my_db)