from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
from agents.jd_analyzer_agent import run_jd_analysis, JobRequirements
from agents.screener_agent import run_screening_pipeline, ScreeningResult
from agents.sourcing_agent import run_sourcing_pipeline, SourcingResults
from agents.interviewer_agent import run_interview_planning_pipeline, InterviewPlan
from agents.utils import parse_agent_output

app = FastAPI(title="TalentStream AI API", description="Autonomous Multi-Agent Hiring System")

class AnalysisRequest(BaseModel):
    jd_text: str

class ScreeningRequest(BaseModel):
    jd_requirements: JobRequirements
    resume_text: str

class EvaluationRequest(BaseModel):
    candidate_name: str
    jd_text: str
    resume_text: str

class EvaluationResponse(BaseModel):
    requirements: JobRequirements
    screening: ScreeningResult
    interview_plan: InterviewPlan

@app.get("/")
async def root():
    return {"message": "Welcome to TalentStream AI API", "status": "active", "version": "1.0.0"}

@app.post("/analyze-jd", response_model=JobRequirements)
async def analyze_jd(request: AnalysisRequest):
    try:
        result = run_jd_analysis(request.jd_text)
        return parse_agent_output(result, JobRequirements)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/source-candidates", response_model=SourcingResults)
async def source_candidates(request: AnalysisRequest):
    """Analyzes a JD and finds matching candidates in the Vector DB."""
    try:
        jd_result = run_jd_analysis(request.jd_text)
        jd_requirements = parse_agent_output(jd_result, JobRequirements)
        sourcing_result = run_sourcing_pipeline(jd_requirements)
        return parse_agent_output(sourcing_result, SourcingResults)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/evaluate-candidate", response_model=EvaluationResponse)
async def evaluate_candidate(request: EvaluationRequest):
    """Runs the full Linear MVP pipeline for a specific candidate."""
    try:
        # 1. Analyze JD
        jd_result = run_jd_analysis(request.jd_text)
        jd_reqs = parse_agent_output(jd_result, JobRequirements)

        # 2. Screen Candidate
        screen_result = run_screening_pipeline(jd_reqs, request.resume_text)
        screen_data = parse_agent_output(screen_result, ScreeningResult)

        # 3. Generate Interview Plan
        interview_result = run_interview_planning_pipeline(request.candidate_name, jd_reqs, screen_data)
        interview_data = parse_agent_output(interview_result, InterviewPlan)

        return EvaluationResponse(
            requirements=jd_reqs,
            screening=screen_data,
            interview_plan=interview_data
        )
    except Exception as e:
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
