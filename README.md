# Expert Persona Chatbot with LangGraph + OpenAI + Google Search

An interactive chatbot built with [LangGraph](https://github.com/langchain-ai/langgraph), powered by **Azure OpenAI** (GPT-4o), enhanced with **Google Custom Search (CSE)** for real-time web access, and fully traceable in [LangSmith](https://smith.langchain.com/).

Supports **expert personas**:

* **FloodRiskExpert** — Miami flood & climate risk advisor
* **AzureAIOpsExpert** — Azure cloud operations & FinOps expert
* **CondoAdvisorExpert** — Miami condo buyer/investor advisor

---

## Features

* **Azure OpenAI GPT-4o** for reasoning & natural dialogue
* **LangGraph orchestration** with memory & tool-calling
* **Google CSE tool** (`web_search`) for fresh, authoritative info
* **Persona-aware prompts** (Flood, Azure, Condo)
* **Streamlit frontend** for a chat UI
* **LangSmith tracing** for detailed run logs and debugging

---

##  Project Structure

```
chatbot/
├─ requirements.txt
├─ .env
├─ langgraph_backend.py     # LangGraph + Azure + Tools + Personas
├─ app.py    # Streamlit chat UI
├─ personas.py              # Persona definitions
└─ tools/
   ├─ google_cse.py         # Low-level Google CSE client
   └─ web_search.py         # LangChain tool wrapper
```

---

## ⚙️ Setup

### 1. Clone repo

```bash
git clone https://github.com/aftabbs/expert-chatbot.git
cd expert-chatbot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

Copy `.env.example` to `.env` and fill values:

```dotenv
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://<your-endpoint>.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o-market
AZURE_OPENAI_API_KEY=YOUR_KEY
AZURE_OPENAI_API_VERSION=2024-05-01-preview

# Google CSE
GOOGLE_API_KEY=YOUR_KEY
GOOGLE_CSE_ID=YOUR_CSE_ID

# LangSmith tracing
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=YOUR_KEY
LANGCHAIN_PROJECT=expert-chatbot
```

---

## Run

### Option 1 — Streamlit UI

```bash
streamlit run streamlit_frontend.py
```

* Select persona from dropdown
* Chat interactively
* Tool calls (e.g. web search) happen transparently

### Option 2 — LangGraph dev server

```bash
langgraph dev
```

* Opens a local API server + LangGraph Studio
* Perfect for debugging workflows

---

## LangSmith Tracing

Every run is logged automatically if `LANGCHAIN_TRACING_V2=true`.

1. Set `LANGCHAIN_API_KEY` in `.env`.
2. Go to [smith.langchain.com](https://smith.langchain.com/)
3. Open your project (`LANGCHAIN_PROJECT`)
4. Inspect runs: inputs, outputs, tool calls, token usage

---
