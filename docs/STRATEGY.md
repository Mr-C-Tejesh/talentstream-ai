# TalentStream AI: Strategy & Roadmap 🗺️

This document serves as the **Architecture Decision Record (ADR)** and **Strategic Roadmap** for TalentStream AI, as established during the project's inception and initial evaluation.

---

## 🧠 1. Strategic Selection: "System over Tool"

**Project Choice:** TalentStream AI – Autonomous Multi-Agent Hiring & Interviewing Engine.

### Why this project?
- **Employer Perspective:** Pivoting from "Applicant" tools (Resume Analyzer) to "Employer" systems demonstrates a higher-level understanding of B2B workflows and ROI.
- **Agentic Reasoning:** Unlike simple keyword matching, this project focuses on **Collaborative Reasoning** where agents debate candidate fit, a cutting-edge requirement in AI engineering.
- **Architectural Maturity:** It utilizes **LangGraph** for stateful, cyclic orchestration, moving beyond basic linear LLM chains.

---

## 📅 2. 8-Week Execution Roadmap

| Phase | Week | Focus | Goal |
| :--- | :--- | :--- | :--- |
| **I: Foundations** | 1-2 | The Core Module | Integrate existing Resume Analyzer. Build the JD Analyzer to extract "Must-Haves." |
| **II: RAG & Search** | 3 | The Sourcing Agent | Set up Vector DB (PostgreSQL + pgvector). Semantic search implementation. |
| **III: Track A MVP** | 4 | Linear Pipeline | **Checkpoint:** Upload Resume -> Score -> Generate 5 Interview Questions. |
| **IV: Agentic Shift**| 5-6 | LangGraph | Implement the "Hiring Committee" debate logic and stateful orchestration. |
| **V: Interaction** | 7 | Voice & Feedback | Add a Simulated Interviewer (Text/Voice) that asks adaptive follow-up questions. |
| **VI: Polishing** | 8 | The "Wow" Factor | Add Bias Detection reports and final deployment on Vercel/Render. |

---

## 🛠️ 3. The Elite Tech Stack

- **Orchestration:** **LangGraph** (for cyclic state management and "debate" loops).
- **LLM:** **Gemini 1.5 Pro** (for 2M+ token context window) and **Groq (Llama 3)** for low-latency screening.
- **Backend:** **FastAPI** (Python).
- **Database:** **PostgreSQL + pgvector** (Industrial standard for combined relational and vector data).
- **Frontend:** **Next.js + Tailwind CSS** (Professional, snappy recruiter dashboard).

---

## 👥 4. Team Role Assignments

- **Lead Architect (Tejesh):** LangGraph implementation, Agent logic, and Backend API structure.
- **Product Engineer (Member 2):** Next.js Frontend & UI/UX; Recruiter Dashboard and Agent Debate visualization.
- **Data & Vector Specialist (Member 3):** PostgreSQL, pgvector, and Resume Parsing; Long-term memory management.
- **Quality & Prompt Engineer (Member 4):** Prompt Engineering (Agent Personalities) and documentation.

---

## 📈 5. Week 1 Review Summary (Status: SUCCESS)

**Key Achievements:**
- ✅ **Modular Architecture:** Established `/agents`, `/docs`, and `/api` scaffolding.
- ✅ **Screener Prototype:** `screener_agent.py` successfully produces structured JSON evaluations.
- ✅ **Defensive Logic:** Implemented robust `parse_result` in `main.py` to handle brittle LLM outputs.
- ✅ **Persona Definition:** Detailed the 4 core personas (Screener, Tech Lead, HR, Manager) in `docs/personas.md`.

**Strategic Note:** The "Digital Hiring Committee" is currently a CLI-based logic; Phase II will focus on moving this into a stateful, searchable system.
