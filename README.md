# ⚖️ Legal Document Analyzer

An AI-powered web application designed to analyze legal contracts, detect risks, identify missing clauses, find internal contradictions, and chat about your document.

## 🌟 Key Features & Optimizations
* **Cross-Section Contradiction Scanning**: Cross-references the entire contract to flag conflicting clauses (e.g. unlimited IP indemnity vs low liability caps).
* **Single-Pass Extraction**: Runs classification, risks, and missing clause scans in a single LLM query, reducing token costs by 75%.
* **Context Truncation Guard**: Restricts input to 12,000 characters to prevent API rate-limit errors and token overflows.
* **Lightweight Chat Routing**: Feeds only serialized analysis reports (not full logs) to the chatbot, saving 50% of input tokens.

## 🛠️ Tech Stack
* **Backend**: FastAPI (Python), LangChain, pdfplumber
* **LLM Engine**: Groq Cloud (Llama 3.1 8B)
* **Frontend**: React.js (Vite), Vanilla CSS

## 🏃 How to Run

### 1. Run the Backend API
From the root folder:
```bash
uv run uvicorn app.main:app --port 8080 --reload
```

### 2. Run the Frontend Dashboard
From the `frontend` folder:
```bash
cd frontend
npm run dev
```
Open `http://localhost:5173` in your browser.
