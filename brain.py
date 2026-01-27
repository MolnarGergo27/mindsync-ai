import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

_embeddings_model = None

def get_embeddings():
    global _embeddings_model
    if _embeddings_model is None:
        _embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return _embeddings_model

def ask_question(query, chat_history, style = "Normál"):
    
    if not os.path.exists("faiss_index"):
        return iter(["Hiba: Még nem tanítottál be dokumentumot. Kérlek, tölts fel egy fájlt az oldalsávon!"]), []    
    
    embeddings = get_embeddings()
    vector_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    
    docs = vector_db.similarity_search(query, k=3)
    context = "\n\n".join([doc.page_content for doc in docs])
    
    sources = []
    for doc in docs:
        page_num = doc.metadata.get("page", "ismeretlen")
        sources.append(f"- Oldal {page_num + 1}")
        
    
    style_prompts = {
        "Normál": "Válaszolj segítőkészen és barátságosan.",
        "Szakmai": "Válaszolj precízen, technikai részletekkel, szaknyelven.",
        "Egyszerű": "Magyarázd el úgy, mintha egy 5 évesnek beszélnél, kerüld a bonyolult szavakat.",
        "Összefoglaló": "Csak a legfontosabb lényeget írd le, pontokba szedve, maximum 3 mondatban."
    }
    
    selected_style = style_prompts.get(style, "Válaszolj segítőkészen")
        
    llm = ChatGroq(temperature=0, model_name="llama-3.1-8b-instant", groq_api_key=os.getenv("GROQ_API_KEY"))
    

    history_str = "\n".join([f"{m['role']}: {m['content']}" for m in chat_history[-3:]])    
    
    prompt = f"""
    Te egy {selected_style} asszisztens vagy. Az alábbi kontextus és előzmények alapján válaszolj.
    
    ELŐZMÉNYEK:
    {history_str}
    
    KONTEXTUS:
    {context}
    
    KÉRDÉS:
    {query}
    """
    
    response = llm.stream(prompt)
    
    return response, list(set(sources))