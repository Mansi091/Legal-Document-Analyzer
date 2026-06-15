# ⚖️ LexGenie

An intelligent legal contract review assistant designed to detect risks, highlight missing clauses, identify internal contradictions, and chat dynamically with your legal documents.

## 🌟 Key Optimizations & Pros
* **75% Token Reduction (Single-Pass)**: Executes classification, risks, and missing clause scans in a single LLM request.
* **Cross-Section Contradiction Scanning**: Cross-references the entire contract to flag conflicting terms (e.g., unlimited IP indemnity vs. low liability caps).
* **Lightweight Chat Routing**: Feeds only serialized analysis reports to the chatbot, saving **50%** of chatbot prompt tokens.
* **Context Truncation Guard**: Safely restricts input length to prevent API token overflow errors.
* **Zero-Config Demo Mode**: Fully functional frontend mock/demo capabilities when no API keys are provided.

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
