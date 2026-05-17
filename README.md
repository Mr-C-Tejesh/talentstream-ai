# TalentStream AI 🚀

**Autonomous Multi-Agent Hiring & Interviewing System**

> Built by **Team Titanic** | Agentic AI Saksham Internship | Capabl × Nasscom

---

## 🔥 What Is TalentStream AI?

TalentStream AI is an autonomous recruitment ecosystem that simulates a **real-world hiring pipeline.** Instead of relying on a single model, it employs a **Digital Hiring Committee** of specialized AI agents that collaborate, debate, and reason together — moving a candidate from raw resume to a final data-driven hiring decision.

**This is not a resume parser. This is a hiring committee.**

---

## 🌐 Live Demo

- **Frontend (Streamlit):** [talentstream-ai.streamlit.app](https://talentstream-ai.streamlit.app)
- **Backend (Railway):** [talentstream-api-production.up.railway.app](https://talentstream-api-production.up.railway.app/health)

---

## 🏗️ System Architecture

```
Streamlit Dashboard
        │
        ▼
FastAPI Backend (Railway)
        │
        ├── JD Analyzer Agent (CrewAI)
        │       └── Extracts Must-Haves, Tech Stack, Requirements
        │
        ├── Technical Screener Agent (CrewAI)
        │       └── Match Score, Strengths, Critical Gaps
        │
        ├── Interviewer Agent (CrewAI)
        │       └── 5 Strategic Non-Googlable Questions
        │
        └── Digital Hiring Committee (LangGraph StateGraph)
                ├── Tech Lead Agent
                ├── HR Specialist Agent
                ├── Department Manager Agent
                └── Consensus → HIRE / INTERVIEW FURTHER / REJECT
```

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| AI Framework | CrewAI + LangGraph |
| LLM | Groq (Llama 3.3 70B + Llama 3.1 8B) |
| Backend | FastAPI |
| Frontend | Streamlit |
| Deployment | Railway (API) + Streamlit Cloud (UI) |

---

## 🎯 Features

| Feature | Description |
|---|---|
| 📄 JD Analysis | Extracts structured Must-Haves from raw job descriptions |
| 🔍 Technical Screening | Semantic resume-JD matching with match probability |
| 🎤 Interview Planning | 5 surgical questions targeting candidate-specific weak spots |
| 🏛️ Hiring Committee | LangGraph debate — Tech Lead, HR Specialist, Department Manager |
| 💬 Simulated Interview | Candidate answers questions and receives real-time AI feedback |

---

## 🚀 How to Run Locally

### 1. Clone and install
```bash
git clone https://github.com/Mr-C-Tejesh/talentstream-ai.git
cd talentstream-ai
pip install -r requirements.txt
```

### 2. Set up environment
```bash
cp .env.example .env
# Add your GROQ_API_KEY to .env
```

### 3. Run CLI demo
```bash
python main.py
```

### 4. Run API backend
```bash
uvicorn api.main:app --reload
```

### 5. Run Streamlit UI
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
talentstream-ai/
├── agents/
│   ├── jd_analyzer_agent.py
│   ├── screener_agent.py
│   ├── interviewer_agent.py
│   └── hiring_committee.py
├── api/
│   └── main.py
├── docs/
│   ├── STRATEGY.md
│   └── personas.md
├── data/Samples/
├── app.py
├── main.py
├── requirements.txt
└── render.yaml
```

---

## 👥 Team Titanic

| Role | Member |
|---|---|
| Captain & Lead Developer | C Tejesh |
| Member | Bhuvan |
| Member | Darshan BR |
| Member | Vinay |

**Institution:** RV Institute of Technology and Management (RVITM), Bengaluru

---

*Built over 8 weeks as part of the Agentic AI Saksham Internship by Capabl × Nasscom*# TalentStream AI 🚀

**Autonomous Multi-Agent Hiring & Interviewing System**

> Built by **Team Titanic** | Agentic AI Saksham Internship | Capabl × Nasscom

---

## 🔥 What Is TalentStream AI?

TalentStream AI is an autonomous recruitment ecosystem that simulates a **real-world hiring pipeline.** Instead of relying on a single model, it employs a **Digital Hiring Committee** of specialized AI agents that collaborate, debate, and reason together — moving a candidate from raw resume to a final data-driven hiring decision.

**This is not a resume parser. This is a hiring committee.**

---

## 🌐 Live Demo

- **Frontend (Streamlit):** [talentstream-ai.streamlit.app](https://talentstream-ai.streamlit.app)
- **Backend (Railway):** [talentstream-api-production.up.railway.app](https://talentstream-api-production.up.railway.app/health)

---

## 🏗️ System Architecture

```
Streamlit Dashboard
        │
        ▼
FastAPI Backend (Railway)
        │
        ├── JD Analyzer Agent (CrewAI)
        │       └── Extracts Must-Haves, Tech Stack, Requirements
        │
        ├── Technical Screener Agent (CrewAI)
        │       └── Match Score, Strengths, Critical Gaps
        │
        ├── Interviewer Agent (CrewAI)
        │       └── 5 Strategic Non-Googlable Questions
        │
        └── Digital Hiring Committee (LangGraph StateGraph)
                ├── Tech Lead Agent
                ├── HR Specialist Agent
                ├── Department Manager Agent
                └── Consensus → HIRE / INTERVIEW FURTHER / REJECT
```

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| AI Framework | CrewAI + LangGraph |
| LLM | Groq (Llama 3.3 70B + Llama 3.1 8B) |
| Backend | FastAPI |
| Frontend | Streamlit |
| Deployment | Railway (API) + Streamlit Cloud (UI) |

---

## 🎯 Features

| Feature | Description |
|---|---|
| 📄 JD Analysis | Extracts structured Must-Haves from raw job descriptions |
| 🔍 Technical Screening | Semantic resume-JD matching with match probability |
| 🎤 Interview Planning | 5 surgical questions targeting candidate-specific weak spots |
| 🏛️ Hiring Committee | LangGraph debate — Tech Lead, HR Specialist, Department Manager |
| 💬 Simulated Interview | Candidate answers questions and receives real-time AI feedback |

---

## 🚀 How to Run Locally

### 1. Clone and install
```bash
git clone https://github.com/Mr-C-Tejesh/talentstream-ai.git
cd talentstream-ai
pip install -r requirements.txt
```

### 2. Set up environment
```bash
cp .env.example .env
# Add your GROQ_API_KEY to .env
```

### 3. Run CLI demo
```bash
python main.py
```

### 4. Run API backend
```bash
uvicorn api.main:app --reload
```

### 5. Run Streamlit UI
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
talentstream-ai/
├── agents/
│   ├── jd_analyzer_agent.py
│   ├── screener_agent.py
│   ├── interviewer_agent.py
│   └── hiring_committee.py
├── api/
│   └── main.py
├── docs/
│   ├── STRATEGY.md
│   └── personas.md
├── data/Samples/
├── app.py
├── main.py
├── requirements.txt
└── render.yaml
```

---

## 👥 Team Titanic

| Role | Member |
|---|---|
| Captain & Lead Developer | C Tejesh |
| Member | Bhuvan |
| Member | Darshan BR |
| Member | Vinay |

**Institution:** RV Institute of Technology and Management (RVITM), Bengaluru

---

*Built over 8 weeks as part of the Agentic AI Saksham Internship by Capabl × Nasscom*