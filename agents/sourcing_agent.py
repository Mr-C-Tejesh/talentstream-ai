from crewai import Agent, Task, Crew, Process
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from .jd_analyzer_agent import JobRequirements
from .vector_db import VectorDB

class CandidateMatch(BaseModel):
    name: str = Field(..., description="Name of the candidate.")
    score: float = Field(..., description="Semantic similarity score (0.0 to 1.0).")
    match_reasoning: str = Field(..., description="Brief reason why this candidate matches the JD.")

class SourcingResults(BaseModel):
    top_candidates: List[CandidateMatch] = Field(..., description="List of top candidates matching the JD.")

class SourcingAgent:
    def __init__(self, model="groq/llama-3.3-70b-versatile"):
        self.agent = Agent(
            role="Expert Headhunter & Talent Scout",
            goal="Identify the best candidates from the internal talent database based on structured job requirements.",
            backstory=(
                "You are an elite headhunter known for finding 'hidden gem' candidates. "
                "You don't just look for keyword matches; you look for depth, potential, and project relevance. "
                "You excel at translating complex job requirements into search strategies."
            ),
            allow_delegation=False,
            verbose=True,
            memory=False,
            llm=model
        )
        self.db = VectorDB()

    def create_task(self, jd_requirements: JobRequirements):
        # Format requirements into a search query string for VectorDB
        search_query = f"Experience with {', '.join(jd_requirements.required_tech_stack)}. "
        search_query += f"Must have: {', '.join(jd_requirements.must_haves)}. "
        search_query += f"Role: {jd_requirements.role_title}."

        return Task(
            description=(
                f"Your task is to review candidates sourced from the database for the following role: **{jd_requirements.role_title}**.\n\n"
                f"**Job Requirements:**\n- Tech Stack: {', '.join(jd_requirements.required_tech_stack)}\n- Must-Haves: {', '.join(jd_requirements.must_haves)}\n\n"
                f"**Search Strategy:** We have performed a semantic search using the query: '{search_query}'.\n\n"
                "Evaluate the candidates provided below and explain why they are a strong fit. "
                "Select the top 3-5 candidates."
            ),
            expected_output="A structured JSON response with the top candidates and the reasoning for their selection.",
            agent=self.agent,
            output_json=SourcingResults
        )

def run_sourcing_pipeline(jd_requirements: JobRequirements, model="groq/llama-3.3-70b-versatile"):
    # 1. Initialize the agent
    sourcer = SourcingAgent(model=model)
    
    # 2. Get candidates from Vector DB
    # Note: In a real scenario, this would be a tool. For simplicity, we fetch them here and pass to the agent.
    search_query = f"Role: {jd_requirements.role_title}. Skills: {', '.join(jd_requirements.required_tech_stack)}"
    raw_results = sourcer.db.search_candidates(search_query, limit=5)
    
    if not raw_results:
        return SourcingResults(top_candidates=[])

    # 3. Format raw results for the agent
    candidate_list_str = ""
    for name, text, metadata, score in raw_results:
        candidate_list_str += f"NAME: {name}\nSCORE: {score:.2f}\nRESUME SUMMARY: {text[:500]}...\n---\n"

    # 4. Create and run task
    task = sourcer.create_task(jd_requirements)
    # Inject the actual results into the task description
    task.description += f"\n\n**Candidates from Database:**\n{candidate_list_str}"
    
    crew = Crew(
        agents=[sourcer.agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True
    )
    
    result = crew.kickoff()
    return result
