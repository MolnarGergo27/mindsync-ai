MindSync AI - RAG-Based Document Intelligence

A MindSync AI egy modern, RAG (Retrieval-Augmented Generation) architektúrára épülő alkalmazás, amely lehetővé teszi a felhasználók számára, hogy privát dokumentumaikból (PDF, DOCX, TXT) egy intelligens tudásbázist építsenek, és azokkal természetes nyelven kommunikáljanak.

Program folyamatai:
1. A felhasználó feltölti a használni kívánt dokumentumot
2. Az AI ezt beolvassa, megjegyzi
3. Majd ezután a felhasználó kiválassza, hogy az AI milyen szerepkörben betöltött szerepként válaszoljon
4. Végül a kérdéseket felteheti az AI-nak


Főbb funkciók:
- Multi-format Ingestion: PDF, Word és TXT fájlokat egyaránt automatikusan feldolgoz és indexel
- Semantic Search: Kulcsszavak helyett kontextus alapú keresést hajt végre FAISS vektoradatbázissal
- Personal-driven Answers: Állítható az AI válaszstílusa (egyszerű, szakmai, összefoglaló)
- Smart Memory: Kontextus-tudatos beszélgetéskezelés
- Source Citations: A dokumentum oldalát megjeleníti ezáltal hitelesebb a válasz
- Streaming UI: Valós idejű válaszadás


Technológiai Stack:
- LLM: Llama 3.1 (Groq Cloud API) - a gyors következtetésért
- Embeddings: HuggingFace a szemantikus reprezentációhoz (all-MiniLM-L6-v2)
- Vector Store: FAISS a nagy teljesítményű kezeléshez
- Orchestration: LangChain a dokumentum-pipeline és a chat-memória kezeléshez
- Frontend: Streamlit egyedi CSS stílusokkal
- DevOps: Docker és Docker Compose a platformfüggetlen futtatáshoz


Gyorsindítás:
1. Repo clone
git clone https://github.com/username/mindsync-ai.git
cd mindsync-ai

2. Env változó létrehozása a gyökérmappába 
GROQ_API_KEY=your_api_key_here

3. Indítás
docker compose up --build

4. Alkamazás elérhető: http://localhost:8501



Native Setup:
1. python -m venv venv
2. .\venv\Scripts\Activate.ps1
3. pip install -r requirements.txt



A fejlesztés menete és kihívások:
A fejlesztés során több kritikus technikai döntést hoztam, amelyek formálták a végleges architektúrát:

1. Vektoradatbázis migráció (ChromaDB -> FAISS):
Eredetileg ChromaDB-t használtam, azonban Windows környezetben a C++ build eszközök és a SQLite verziókörnyezet inkompatibilitása miatt a telepítés nem volt elég robusztus. A FAISS-re való váltás mellett döntöttem, ami javította a stabilitást és gyorsabb válaszidőt eredményezett lokális indexelésnél.

2. Chunking stratégia:
A dokumentumok feldolgozásánál 1000 karakteres ablakokat használtam 100 karakteres átfedéssel. Ez biztosította, hogy a szemantikus jelentés ne vesszen el a darabolás mentén, így az AI pontosabb kontextust kap.

3. Modell management:
A kiinduló terv, hogy a ChatGPT 4o-s modell használata, de későbbiekben proaktívan frissítettem a rendszert Llama 3.1-re, a költséghatékonyság és az open-source rugalmasság végett, amit a Groq Cloud biztosít.


Projekt struktúra:
.
├── faiss_index/        # Helyi vektor adatbázis
├── app.py              # Streamlit frontend
├── brain.py            # RAG logika és LLM hívások
├── ingest.py           # Dokumentum feldolgozás
├── Dockerfile          # Konténer definíció
├── docker-compose.yml  # Multi-konténer setup
└── requirements.txt    # Függőségek

![MindSync AI Főoldal](default.png)
![Működése](processing.png)

Készítette: Molnár Gergő - https://www.linkedin.com/in/gerg%C5%91-moln%C3%A1r-3920b53a7/
