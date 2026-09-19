
# HR & Recruitment RAG Chatbot

A document-based HR and recruitment chatbot built with Python, Streamlit, Google Gemini, and ChromaDB.

The chatbot retrieves relevant information from a collection of HR and recruitment documents and uses that context to generate answers. It is designed to answer questions grounded in the available documents and refuse unrelated questions when they fall outside its scope.

## Project Overview

This project explores how Retrieval-Augmented Generation (RAG) can support HR and recruitment information access.

### Key Features

- Document-based question answering
- Semantic retrieval using embeddings
- Google Gemini-powered response generation
- ChromaDB vector database
- Streamlit chat interface
- Source-document display
- Configurable retrieval relevance cutoff
- Out-of-scope refusal and prompt-injection testing

## Technology Stack

- Python
- Streamlit
- Google Gemini API
- ChromaDB
- Document embeddings and retrieval

## Project Structure

```text
hr-chatbot/
├── app.py
├── config.py
├── ingest.py
├── rag_core.py
├── check_setup.py
├── requirements.txt
├── source_log.md
├── .gitignore
├── data/                 # Local documents for ingestion
└── sets/                 # Collected source-document sets
```

The ChromaDB database is generated locally during ingestion and is not intended to be committed to GitHub.

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/thanujathanuja037-lab/hr-recruitment-rag-chatbot
cd hr-recruitment-rag-chatbot
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure the Gemini API key

api key is created


### 5. Add documents and build the index
 to query in the input folder expected by `ingest.py`.

Run the ingestion script:

```powershell
python ingest.py
```

This creates or updates the local vector database used for retrieval.

### 6. Run the chatbot

```powershell
python -m streamlit run app.py
```

Open the local URL displayed in the terminal.

## Evaluation

The prototype is being evaluated using HR/recruitment questions, out-of-scope questions, and prompt-injection attempts.

Evaluation outcomes are recorded separately. Results should be interpreted as preliminary manual testing, not as a guarantee of accuracy, security, or production readiness.

## Limitations

- Answers depend on the coverage and quality of the supplied documents.
- Retrieval may miss relevant information or return incomplete context.
- Generated answers require human verification.
- The prototype is not a substitute for official HR policies or professional HR judgment.
- It is an academic prototype, not a production recruitment or applicant-tracking system.

## Data and Sources

The repository includes collected source documents for experimentation. Refer to `source_log.md` for source information.

## Disclaimer

This project was developed for academic and learning purposes. It is not an official GitLab or SRMIST product, and it is not affiliated with or endorsed by those organizations.
