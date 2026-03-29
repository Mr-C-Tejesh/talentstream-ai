from crewai import Agent, Task, Crew, Process
from pydantic import BaseModel, Field
from typing import List, Optional
from .jd_analyzer_agent import JobRequirements
import os

class ScreeningResult(BaseModel):
    match_percentage: int = Field(..., description="The percentage match between the resume and JD (0-100).")
    key_strengths: List[str] = Field(..., description="Top 3-5 technical or professional strengths identified.")
    areas_to_probe: List[str] = Field(..., description="3-5 specific questions or areas for the interviewer to explore.")
    candidate_summary: str = Field(..., description="A 2-3 sentence summary of the candidate's profile.")
    missing_skills: List[str] = Field(..., description="List of critical skills or requirements from JD missing in resume.")

class ScreenerAgent:
    def __init__(self, model="groq/llama-3.3-70b-versatile"):
        self.agent = Agent(
            role="Expert Technical Recruiter & Resume Analyst",
            goal="Perform a deep match between a candidate's resume and structured job requirements.",
            backstory=(
                "You are a seasoned technical recruiter with 15+ years of experience in FAANG-level hiring. "
                "You have a keen eye for detail and can spot technical depth, architectural understanding, "
                "and potential red flags that non-technical recruiters might miss. "
                "You focus on quantifiable impact rather than just keywords."
            ),
            allow_delegation=False,
            verbose=True,
            memory=False,
            llm=model
        )

    def create_task(self, jd_requirements: JobRequirements, resume_text: str):
        from datetime import date
        current_date = date.today().strftime("%Y-%m-%d")
        
        # Format requirements for the prompt
        must_haves_str = "\n".join([f"- {m}" for m in jd_requirements.must_haves])
        tech_stack_str = ", ".join(jd_requirements.required_tech_stack)
        
        return Task(
            description=(
                f"Important Context: The current date is {current_date}. Use this date to accurately calculate the total years of work experience when a candidate lists 'Present'.\n\n"
                f"Analyze the following Resume against the structured Job Requirements for the role: **{jd_requirements.role_title}**.\n\n"
                f"**Critical Must-Haves:**\n{must_haves_str}\n\n"
                f"**Required Tech Stack:**\n{tech_stack_str}\n\n"
                f"**Resume Content:**\n{resume_text}\n\n"
                "Extract the match percentage, key strengths, areas to probe, a brief candidate summary, "
                "and any missing critical skills based on the Must-Haves and Tech Stack provided."
            ),
            expected_output="A structured JSON response with match_percentage, key_strengths, areas_to_probe, candidate_summary, and missing_skills.",
            agent=self.agent,
            output_json=ScreeningResult
        )

def run_screening_pipeline(jd_requirements: JobRequirements, resume_text: str, model="groq/llama-3.3-70b-versatile"):
    # Initialize the agent
    screener = ScreenerAgent(model=model)
    
    # Create the task
    task = screener.create_task(jd_requirements, resume_text)
    
    # Assemble the crew
    crew = Crew(
        agents=[screener.agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
        memory=False
    )
    
    # Execute the pipeline
    result = crew.kickoff()
    return result
