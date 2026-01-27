import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from dotenv import load_dotenv
from brain import get_embeddings

load_dotenv() 

def process_document(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    
    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext == ".docx" or ext == ".doc":
        loader = Docx2txtLoader(file_path)
    elif ext == ".txt":
        loader = TextLoader(file_path, encoding="utf-8")
    else:
        raise ValueError(f"Nem támogatott fájlformátum: {ext}")

    data = loader.load()
    
    # Dokumentum feldarabolása
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(data)
    
    # Beágyazások létrehozása
    embeddings = get_embeddings()
    
    # Vektor adatbázis létrehozása és mentése
    vector_db = FAISS.from_documents(documents=chunks, embedding=embeddings)
    vector_db.save_local("faiss_index")
    print("Sikeres beolvasás és indexelés.")