MindSync AI - RAG-Based Document Intelligence

MindSync AI is a modern application built on RAG (Retrieval-Augmented Generation) architecture. It allows users to build an intelligent knowledge base from private documents (PDF, DOCX, TXT) and interact with them using natural language.

Workflow:
1. Upload: User uploads the desired documents.
2. Ingestion: The AI reads and indexes the content.
3. Persona Selection: User selects a specific role/persona for the AI to adopt.
4. Interaction: User queries the AI based on the provided documents.


Key features:
- Multi-format Ingestion: Automatically processes and indexes PDF, Word, and TXT files.
- Semantic Search: Executes context-based searches using a FAISS vector database instead of simple keyword matching.
- Personal-driven Answers: Adjustable response styles (Simple, Professional, or Summary).
- Smart Memory: Context-aware conversation management.
- Source Citations: Displays specific document pages to ensure transparency and credibility.
- Streaming UI: Real-time response generation for a fluid user experience
- Image Extraction: Extracts, describes, and summarizes images within documents, treating visual data with the same depth as text.


Tech Stack:
- LLM: Llama 3.1 (via Groq Cloud API) – for ultra-fast inference.
- Embeddings: HuggingFace for semantic representation. (all-MiniLM-L6-v2)
- Vector Store: FAISS for high-performance vector management.
- Orchestration: LangChain for document pipelines and chat memory management.
- Frontend: Streamlit with custom CSS styling.
- DevOps: Docker & Docker Compose for platform-independent deployment.


Quick Start:
1. Clone the Repository
git clone https://github.com/username/mindsync-ai.git
cd mindsync-ai

2. Configure Environment Variables
GROQ_API_KEY=your_api_key_here

3. Launch via Docker
docker compose up --build

4. The application will be available at: http://localhost:8501



Native Setup:
1. python -m venv venv
2. .\venv\Scripts\Activate.ps1
3. pip install -r requirements.txt



Development Process & Challenges:
During development, several critical technical decisions were made to shape the final architecture:

1. Vector Database Migration (ChromaDB -> FAISS):
Originally, I utilized ChromaDB. However, due to incompatibilities between C++ build tools and SQLite versions in Windows environments, the setup wasn't robust enough. I migrated to FAISS, which improved stability and resulted in faster local indexing response times.

2. Chunking Strategy:
For document processing, I implemented a strategy using 1,000-character windows with a 100-character overlap. This ensures that semantic meaning is preserved across chunks, providing the AI with more accurate context.

3. Model Management:
The initial plan involved GPT-4o. However, I proactively updated the system to Llama 3.1 via Groq Cloud to leverage open-source flexibility and significantly higher cost-efficiency without sacrificing performance.

4. Image Processing:
I integrated the Llama 3.2 Vision (or Llama 4 Scout as referenced) model through Groq’s efficient API. During ingestion, the system automatically extracts images from documents and generates detailed textual descriptions. This data is stored in the vector database, allowing users to query the AI about visual content within the files.

Project Structure:
.
├── faiss_index/        # Local vector database
├── app.py              # Streamlit frontend
├── brain.py            # RAG logic és LLM calls
├── ingest.py           # Document processing pipeline
├── Dockerfile          # Container definition
├── docker-compose.yml  # Multi-container setup
└── requirements.txt    # Project Dependencies

![MindSync AI Main Page](default.png)
![Operation](processing.png)

Created by: Molnár Gergő - https://www.linkedin.com/in/gerg%C5%91-moln%C3%A1r-3920b53a7/
