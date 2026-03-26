# TalentStream AI 🚀

**Autonomous Multi-Agent Hiring & Interviewing System**

TalentStream AI is an autonomous recruitment ecosystem powered by a "Digital Hiring Committee." It employs a multi-agent architecture where specialized AI agents collaborate to move a candidate from application to final decision.

## 🧠 System Architecture

The system operates on an Orchestrated Agentic Workflow:
1. **Ingestion Layer**: Job Description (JD) and Resume (PDF) are parsed.
2. **Screening Agent**: Performs a "Deep Match" between the JD requirements and the candidate’s experience.
3. **The Interviewer (Interactive Agent)**: A dynamic chat interface where the agent probes "weak spots" identified during screening.
4. **The Committee (Debate Layer)**: The interview transcript is passed to three agents (Tech Lead, HR Specialist, Department Manager).
5. **Consensus Engine**: Agents resolve conflicts and output a final "Talent Report."

## 🧩 Project Structure
- `agents/`: Core logic for specialized AI agents.
- `api/`: FastAPI backend for the recruiter dashboard.
- `docs/`: Personas, technical diagrams, and project documentation.
- `tests/`: Unit and integration tests.
- `main.py`: CLI entry point for testing the pipeline.

## 🛠️ Tech Stack
- **AI Framework**: CrewAI / LangGraph
- **LLMs**: GPT-4o & Claude 3.5 Sonnet
- **Backend**: FastAPI (Python)
- **Frontend**: Next.js (Tailwind CSS)
- **Database**: PostgreSQL & Pinecone

## 🚀 Getting Started (Week 1)
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the Screener Demo:
   ```bash
   python main.py
   ```
