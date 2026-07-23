# RAG Pipeline

This project is a small retrieval-augmented generation (RAG) demo built around local document ingestion, embedding generation, vector search, and LLM-based summarization.

## What It Does

- Loads supported documents from the `data/` folder.
- Chunks documents into smaller passages.
- Generates embeddings with `sentence-transformers`.
- Stores vectors in a FAISS index.
- Retrieves relevant chunks for a user query.
- Sends retrieved context to Groq for summarization or answer generation.

## Project Layout

- `main.py` - runs a simple search-and-summarize example.
- `src/data_loader.py` - document loading utilities.
- `src/embedding.py` - text chunking and embedding pipeline.
- `src/vectorstore.py` - FAISS vector store wrapper.
- `src/search.py` - retrieval and RAG helpers.
- `src/ingest.py` - incremental ingestion for new files.
- `data/` - source documents and persisted vector data.
- `notebook/` - notebook experiments and walkthroughs.

## Requirements

- Python 3.12+
- A virtual environment named `rag_env`
- `GROQ_API_KEY` in a local `.env` file for LLM calls

## Setup

```powershell
python -m venv rag_env
rag_env\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the project root if you want to use the Groq-powered RAG flow:

```env
GROQ_API_KEY=your_key_here
```

## Usage

Run the demo search flow:

```powershell
python main.py
```

Ingest new files from `data/` into the existing FAISS store:

```powershell
python src/ingest.py
```

## Supported Data Files

The ingestion pipeline supports:

- PDF
- TXT
- CSV
- XLSX
- DOCX
- JSON

## Notes

- The vector store is persisted under `faiss_store/`.
- The ingestion script tracks indexed files in `faiss_store/indexed_files.json`.
- The notebook in `notebook/pdf_loader.ipynb` is useful for step-by-step experimentation, but the reusable logic lives in `src/`.
