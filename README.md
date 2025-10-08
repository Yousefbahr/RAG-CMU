# RAG-CMU
A RAG system built from scratch, capable of answering questions about Pittsburgh and CMU.

Assignment 2 of CMU: Advanced NLP Spring 2024.

## Usage
```
docker build -t rag-chatbot .

docker run -d -p 8000:8000 rag-chatbot
```
Access it at http://localhost:8000

---
## Features

- **Retrieval-Augmented Generation (RAG):** Combines document retrieval and generation for accurate, context-aware responses.  
- **FastAPI Backend:** Manages request routing, LLM inference, and response handling efficiently.  
- **LangChain Integration:** Handles retrieval chains, prompt templates, and context injection.  
- **Dynamic Data Extraction:** Uses **BeautifulSoup** and **pdfplumber** to scrape and parse websites and PDF documents.  
- **Chroma Vector Store:** Efficiently stores and retrieves document embeddings for fast, semantic search.  
- **Dockerized Application:** Fully containerized setup for consistent deployment across environments.
---

## Project Structure
```
├── app
│   ├── core
│   │   ├── __init__.py
│   │   ├── llm.py
│   │   ├── prompts.py
│   │   └── retriever.py
│   ├── __init__.py
│   ├── main.py
├── chroma_langchain_db
│   │   ├── ...
│   └── chroma.sqlite3
├── data
│   ├── test
│   │   ├── questions.txt
│   │   └── reference_answers.txt
│   └── train
│       ├── questions.txt
│       └── reference_answers.txt
├── Dockerfile
├── documents
│   ├── Events
│   │   ├── ...
│   ├── food_festivals
│   │   ├── ...
│   ├── General_Info_&_History
│   │   ├── ...
│   ├── Museums
│   │   ├── ...
│   ├── Music
│   │   ├── ...
│   ├── Operating_Budget
│   │   ├── ...
│   ├── sports
│   │   ├── ...
│   └── tax
│   │   ├── ...
├── LICENSE
├── notebooks
│   ├── Chunking.ipynb
│   ├── processing_documents.ipynb
│   └── Web_Scraping.ipynb
├── README.md
├── requirements.txt
├── static
│   └── script.js
└── templates
    └── index.html
```
