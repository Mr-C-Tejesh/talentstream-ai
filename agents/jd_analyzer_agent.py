from crewai import Agent, Task, Crew, Process
from pydantic import BaseModel, Field
from typing import List, Optional

class JobRequirements(BaseModel):
    role_title: str = Field(..., description="The official title of the job role.")
    min_years_experience: int = Field(..., description="The minimum years of experience required (if specified).")
    required_tech_stack: List[str] = Field(..., description="Core technical skills and languages explicitly required.")
    soft_skills: List[str] = Field(..., description="Key soft skills and leadership traits sought.")
    must_haves: List[str] = Field(..., description="Non-negotiable critical technical or domain requirements.")
    preferred_qualifications: List[str] = Field(..., description="Optional but highly valued skills or experiences.")

class JDAnalyzerAgent:
    def __init__(self, model="groq/llama-3.3-70b-versatile"):
        self.agent = Agent(
            role="Technical Hiring Strategist",
            goal="Analyze a Job Description (JD) and extract a structured set of core requirements and 'Must-Haves'.",
            backstory=(
                "You are an expert at decoding job descriptions. You can distinguish between 'nice-to-have' "
                "buzzwords and the actual core technical requirements that define a successful hire. "
                "Your output serves as the source of truth for the screening and interview process."
            ),
            allow_delegation=False,
            verbose=True,
            memory=False,
            llm=model
        )

    def create_task(self, jd_text: str):
        return Task(
            description=(
                "Analyze the following Job Description (JD) and extract a structured set of requirements.\n\n"
                f"**Job Description:**\n{jd_text}\n\n"
                "Focus on identifying the core technical stack, minimum experience, and critical 'must-have' skills "
                "that are non-negotiable for this role. Distinguish these from preferred qualifications."
            ),
            expected_output="A structured JSON response with role_title, min_years_experience, required_tech_stack, soft_skills, must_haves, and preferred_qualifications.",
            agent=self.agent,
            output_json=JobRequirements
        )

def run_jd_analysis(jd_text: str, model="groq/llama-3.3-70b-versatile"):
    # Initialize the agent
    analyzer = JDAnalyzerAgent(model=model)
    
    # Create the task
    task = analyzer.create_task(jd_text)
    
    # Assemble the crew
    crew = Crew(
        agents=[analyzer.agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
        memory=False
    )
    
    # Execute the pipeline
    result = crew.kickoff()
    return result
