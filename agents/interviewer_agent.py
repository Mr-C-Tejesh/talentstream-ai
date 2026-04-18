from crewai import Agent, Task, Crew, Process
from pydantic import BaseModel, Field
from typing import List, Optional
from .jd_analyzer_agent import JobRequirements
from .screener_agent import ScreeningResult

class InterviewPlan(BaseModel):
    candidate_name: str = Field(..., description="Name of the candidate.")
    overall_score: int = Field(..., description="Final match score (0-100).")
    strategic_questions: List[str] = Field(..., description="5 specific, deep-dive interview questions tailored to the candidate's profile and gaps.")
    interviewer_guidance: str = Field(..., description="Brief tips for the interviewer on how to handle this specific candidate.")

class InterviewerAgent:
    def __init__(self, model="groq/llama-3.3-70b-versatile"):
        self.agent = Agent(
            role="Senior Technical Interviewer & Systems Architect",
            goal="Generate a strategic interview plan with 5 deep-dive questions based on candidate screening results.",
            backstory=(
                "You are a master technical interviewer who has conducted thousands of interviews for "
                "Staff-level roles. You know how to spot 'keyword stuffing' and 'shallow knowledge'. "
                "Your questions are designed to test first-principles thinking and practical problem-solving "
                "rather than theoretical definitions."
            ),
            allow_delegation=False,
            verbose=True,
            memory=False,
            llm=model
        )

    def create_task(self, candidate_name: str, jd_requirements: JobRequirements, screening_result: ScreeningResult):
        # Format probe areas for the prompt
        probe_areas_str = "\n".join([f"- {p}" for p in screening_result.areas_to_probe])
        
        return Task(
            description=(
                f"Your task is to prepare a technical interview plan for **{candidate_name}** for the role of **{jd_requirements.role_title}**.\n\n"
                f"**Screening Report Summary:**\n{screening_result.candidate_summary}\n\n"
                f"**Identified Probe Areas (Weak Spots/Ambiguities):**\n{probe_areas_str}\n\n"
                "Based on the above, generate exactly **5 strategic interview questions**. "
                "These should be high-impact, situational, or architectural questions that force the candidate "
                "to demonstrate depth in the areas where they appeared weak or vague during screening."
            ),
            expected_output="A structured JSON response with candidate_name, overall_score, 5 strategic_questions, and interviewer_guidance.",
            agent=self.agent,
            output_json=InterviewPlan
        )

def run_interview_planning_pipeline(candidate_name: str, jd_requirements: JobRequirements, screening_result: ScreeningResult, model="groq/llama-3.3-70b-versatile"):
    # Initialize the agent
    interviewer = InterviewerAgent(model=model)
    
    # Create the task
    task = interviewer.create_task(candidate_name, jd_requirements, screening_result)
    
    # Assemble the crew
    crew = Crew(
        agents=[interviewer.agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True
    )
    
    # Execute
    result = crew.kickoff()
    return result
