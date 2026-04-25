import os
import fitz 
import base64
from langchain_core.documents import Document  
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from dotenv import load_dotenv
from brain import get_embeddings

load_dotenv() 

def summarize_image_with_groq(image_bytes):
    encoded_image = base64.b64encode(image_bytes).decode('utf-8')
    
    chat = ChatGroq(temperature=0, model_name="meta-llama/llama-4-scout-17b-16e-instruct", groq_api_key=os.getenv("GROQ_API_KEY"))
    
    msg = chat.invoke([
        HumanMessage(content=[
            {"type": "text", "text": "Kérlek, írd le részletesen, mi látható ezen a képen/grafikonon! Foglald össze a kulcsfontosságú adatokat vagy trendeket, hogy később információként kereshető legyen."},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
        ])
    ])
    
    return msg.content

def process_document(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    data = []
    
    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
        data = loader.load()
        
        doc = fitz.open(file_path)
        for page_num in range(len(doc)):
            page = doc[page_num]
            image_list = page.get_images(full=True)
            
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                
                try:
                    print(f"{page_num + 1}. oldalon található kép elemzése folyamatban...")
                    description = summarize_image_with_groq(image_bytes)
                    
                    # Hozzáadjuk a tudásbázishoz virtuális dokumentumként
                    data.append(Document(
                        page_content=f"[KÉP A(z) {page_num + 1}. OLDALON]: {description}",
                        metadata={"page": page_num, "source": file_path, "type": "image_summary"}
                    ))
                except Exception as e:
                    print(f"Hiba a(z) {page_num + 1}. oldalon található kép elemzése során: {e}")
    elif ext == ".docx" or ext == ".doc":
        loader = Docx2txtLoader(file_path)
        data = loader.load()
    elif ext == ".txt":
        loader = TextLoader(file_path, encoding="utf-8")
        data = loader.load()
    else:
        raise ValueError(f"Nem támogatott fájlformátum: {ext}")
    
    # Dokumentum feldarabolása
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(data)
    
    # Beágyazások létrehozása
    embeddings = get_embeddings()
    
    # Vektor adatbázis létrehozása és mentése
    vector_db = FAISS.from_documents(documents=chunks, embedding=embeddings)
    vector_db.save_local("faiss_index")
    print("Sikeres beolvasás és indexelés.")