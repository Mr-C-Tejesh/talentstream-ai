from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

from agents.jd_analyzer_agent import run_jd_analysis, JobRequirements
from agents.screener_agent import run_screening_pipeline, ScreeningResult
from agents.sourcing_agent import run_sourcing_pipeline, SourcingResults
from agents.interviewer_agent import run_interview_planning_pipeline, InterviewPlan
from agents.hiring_committee import run_hiring_committee
from agents.utils import parse_agent_output

app = FastAPI(title="TalentStream AI API", description="Autonomous Multi-Agent Hiring System")

# Ensure API Key is present
if not os.getenv("GROQ_API_KEY"):
    print("⚠️ WARNING: GROQ_API_KEY not found in environment variables!")

class AnalysisRequest(BaseModel):
    jd_text: str

class ScreeningRequest(BaseModel):
    jd_requirements: JobRequirements
    resume_text: str

class EvaluationRequest(BaseModel):
    candidate_name: str
    jd_text: str
    resume_text: str

class CommitteeRequest(BaseModel):
    resume_text: str
    jd_text: str
    screener_summary: str

class EvaluationResponse(BaseModel):
    requirements: JobRequirements
    screening: ScreeningResult
    interview_plan: InterviewPlan
    committee_debate: Optional[Dict] = None

@app.get("/")
async def root():
    return {"message": "Welcome to TalentStream AI API", "status": "active", "version": "1.0.0"}

@app.post("/analyze-jd", response_model=JobRequirements)
def analyze_jd(request: AnalysisRequest):
    try:
        result = run_jd_analysis(request.jd_text)
        return parse_agent_output(result, JobRequirements)
    except Exception as e:
        print(f"ERROR in /analyze-jd: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/hiring-committee")
def hiring_committee(request: CommitteeRequest):
    try:
        result = run_hiring_committee(
            resume=request.resume_text,
            jd=request.jd_text,
            screener_analysis=request.screener_summary
        )
        return result
    except Exception as e:
        print(f"ERROR in /hiring-committee: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/evaluate-candidate", response_model=EvaluationResponse)
def evaluate_candidate(request: EvaluationRequest):
    """Runs the full Agentic pipeline for a specific candidate."""
    try:
        print(f"Starting evaluation for {request.candidate_name}...")
        # 1. Analyze JD
        print("  - Analyzing JD...")
        jd_result = run_jd_analysis(request.jd_text)
        jd_reqs = parse_agent_output(jd_result, JobRequirements)

        # 2. Screen Candidate
        print("  - Screening candidate...")
        screen_result = run_screening_pipeline(jd_reqs, request.resume_text)
        screen_data = parse_agent_output(screen_result, ScreeningResult)

        # 3. Generate Interview Plan
        print("  - Generating interview plan...")
        interview_result = run_interview_planning_pipeline(request.candidate_name, jd_reqs, screen_data)
        interview_data = parse_agent_output(interview_result, InterviewPlan)

        # 4. Run Hiring Committee Debate
        print("  - Convening hiring committee...")
        screener_summary = screen_data.candidate_summary + "\nStrengths: " + ", ".join(screen_data.key_strengths)
        committee_result = run_hiring_committee(
            resume=request.resume_text,
            jd=request.jd_text,
            screener_analysis=screener_summary
        )

        print("Evaluation complete.")
        return EvaluationResponse(
            requirements=jd_reqs,
            screening=screen_data,
            interview_plan=interview_data,
            committee_debate=committee_result
        )
    except Exception as e:
        import traceback
        print(f"ERROR in /evaluate-candidate: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/screen-candidate", response_model=ScreeningResult)
async def screen_candidate(request: ScreeningRequest):
    try:
        result = run_screening_pipeline(request.jd_requirements, request.resume_text)
        return parse_agent_output(result, ScreeningResult)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
