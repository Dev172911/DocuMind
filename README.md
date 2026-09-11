# 🧠 DocuMind

A RAG-powered document question answering app built with Streamlit, LangChain, FAISS, and Groq.

## What it does
- Upload a PDF or DOCX document
- Ask questions about its contents
- Get AI-powered answers with source page references
- View and manage chat history
- Export chats as DOCX

## Tech Stack
- **Frontend** — Streamlit
- **LLM** — Groq (LLaMA3)
- **Embeddings** — HuggingFace sentence-transformers
- **Vector Store** — FAISS
- **Document Loading** — LangChain PyPDFLoader, Docx2txtLoader

## Project Structure

DocuMind/
├── app.py # Main Streamlit app
├── document_loader.py # PDF and DOCX loading
├── text_splitter.py # Chunk splitting
├── vector_store.py # FAISS embeddings and retrieval
├── rag_pipeline.py # Groq LLM and answer generation
├── source_reference.py # Page number extraction
├── export_chat.py # DOCX export
├── config.py # API key config
├── requirements.txt # Dependencies
└── .env # Your API keys (never share this)


## Setup and Run

### 1. Clone the repo

git clone https://github.com/Dev172911/DocuMind.git
cd DocuMind


### 2. Create a virtual environment

python -m venv .venv
source .venv/bin/activate


### 3. Install dependencies

pip install -r requirements.txt


### 4. Create your `.env` file

GROQ_API_KEY=your_groq_api_key_here

Get your free Groq API key at https://console.groq.com

### 5. Run the app

streamlit run app.py


## Notes
- My `.env` file is never pushed to GitHub
- The `vector_db/` folder is also excluded from the repo
- Each user needs their own Groq API key