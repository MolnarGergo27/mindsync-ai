import streamlit as st
import os
import tempfile
from ingest import process_document
from brain import ask_question

st.set_page_config(page_title="MindSync AI", page_icon="🧠", layout="centered")

if "processing" not in st.session_state:
    st.session_state.processing = False
    
if "messages" not in st.session_state:
    st.session_state.messages = []

# CSS stílusok (maradt az eredeti, mert szuper)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #238636; color: white; border: none; }
    .stButton>button:hover { background-color: #2ea043; }
    h1, h2, h3 { color: #58a6ff; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 MindSync AI")

# 1. Sidebar
with st.sidebar:
    st.header("Beállítások")
    uploaded_file = st.file_uploader("Tölts fel egy fájlt", type=["pdf", "docx", "txt"])
    
    answer_style = st.select_slider("Válasz stílusa", 
                                   options=["Normál", "Szakmai", "Egyszerű", "Összefoglaló"], 
                                   value="Normál")
    
    if st.button("Feldolgozás és Tanulás"):
        if uploaded_file:
            st.session_state.processing = True
            st.session_state.messages = [] 
            st.rerun()
        else:
            st.error("Kérlek, tölts fel egy fájlt előbb!")

if st.session_state.processing and uploaded_file:
    with st.spinner("Az AI éppen elemzi a szöveget..."):
        # Csak egy ideiglenes fájlt használunk, nem kell a data mappába is másolni
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            temp_file_path = tmp_file.name
        
        try:
            process_document(temp_file_path)
            st.success(f"Sikeresen megtanultam: {uploaded_file.name}")
        except Exception as e:
            st.error(f"Hiba a feldolgozás során: {e}")
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            st.session_state.processing = False
    
    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Chat kezelése
if prompt := st.chat_input("Kérdezz bármit a dokumentumról...", disabled=st.session_state.processing):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Átadjuk az előzményeket (az utolsó, épp hozzáadott üzenet nélkül)
        response_stream, sources = ask_question(prompt, st.session_state.messages[:-1], style=answer_style)
        
        full_response = st.write_stream(response_stream)
        
        if sources:
            # Szebb megjelenítés a forrásoknak
            source_text = ", ".join([s.replace("- ", "") for s in sources])
            st.caption(f"Források: {source_text}")
                
        st.session_state.messages.append({"role": "assistant", "content": full_response})