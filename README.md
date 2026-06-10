# ⚖️ Legal Document Analyzer

An AI-powered web application designed to analyze legal contracts, detect potential risks, identify missing clauses, find internal contradictions, and allow you to ask questions about the document through an interactive chatbot.

This application acts as an **AI-first triage layer** for founders, sales reps, and freelancers, allowing them to review contracts in seconds instead of spending ₹25,000+ on initial manual lawyer consultations.

---

## 🌟 What Makes This Project Stand Out?

### 1. Logical Cross-Section Contradiction Detection
Most basic AI PDF readers scan paragraphs in isolation. This engine cross-references different sections. For example, if **Section 5** specifies *unlimited* intellectual property liability, but **Section 10** caps *all* liability under the contract to **₹5,00,000**, the system flags this hidden conflict immediately.

### 2. Proactive "Missing Clause" Helper
Instead of just warning you that a standard clause is missing, it provides:
* **Risk Explanation**: Why the missing clause leaves you exposed.
* **Actionable Boilerplate**: Generates a standard, legally sound clause that you can copy and paste directly into your contract draft.

### 3. Dual-Context Chat Panel
The integrated chat assistant does not just look at the raw PDF; it is fully context-aware of the review agent's output. When you ask questions like *"Why is the liability cap too low?"* or *"Rewrite Section 10,"* it answers dynamically by combining the PDF text with the flagged analysis.

---

## ⚡ Under the Hood: Token & Performance Optimizations
Designed with API rate limits (e.g., Groq's low free-tier Token-Per-Minute boundaries) and latency reduction in mind:

* **Single-Pass Structured Extraction**: Performs classification, risk scanning, contradiction detection, and missing clause generation in **one single LLM query**. This cuts API latency by 75% and prevents repetitive input token bills.
* **Context Truncation Guard**: Implements a strict 12,000-character safety guard. If a user uploads a massive contract, it safely truncates the file with an audit log to prevent API context overflows or rate-limit blockages.
* **Lightweight Chat Payload Routing**: Instead of sending verbose step-by-step logs into the chat context, it serializes only the structured findings (`risks`, `missing_clauses`, `contradictions`). This saves up to 50% on input tokens during chatbot interaction.

---

## 🛠️ Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Backend API** | **FastAPI** (Python) | High-performance asynchronous endpoint handler |
| **LLM Engine** | **Groq Cloud** (Llama 3.1 8B) | Hardware-accelerated, sub-second AI inference |
| **Orchestration** | **LangChain** | prompt chaining, history management, and LLM schemas |
| **Frontend UI** | **React.js** (Vite) | Fast-building single page application |
| **PDF Parser** | **pdfplumber** | Accurate textual data extraction from document layers |
| **Styling** | **Vanilla CSS** | Premium custom design system with custom tokens |

---

## 🏃 How to Run the Project

### 1. Run the Backend API
From the root folder:
```bash
# Start FastAPI backend
uv run uvicorn app.main:app --port 8080 --reload
```

### 2. Run the Frontend Dashboard
From the `frontend` folder:
```bash
cd frontend
npm run dev
```
Open `http://localhost:5173` in your browser.
