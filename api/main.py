from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
from agents.jd_analyzer_agent import run_jd_analysis, JobRequirements
from agents.screener_agent import run_screening_pipeline, ScreeningResult
from agents.utils import parse_agent_output

app = FastAPI(title="TalentStream AI API", description="Autonomous Multi-Agent Hiring System")

class AnalysisRequest(BaseModel):
    jd_text: str

class ScreeningRequest(BaseModel):
    jd_requirements: JobRequirements
    resume_text: str

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
