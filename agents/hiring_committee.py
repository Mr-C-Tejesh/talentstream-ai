import os
from typing import List, Dict, TypedDict, Annotated, Union
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field

# Define the state
class HiringCommitteeState(TypedDict):
    resume: str
    jd: str
    screener_analysis: str
    tech_lead_eval: str
    hr_eval: str
    manager_decision: str
    debate_history: List[str]

# Initialize LLM
def get_llm(model_name="llama-3.3-70b-versatile"):
    return ChatOpenAI(
        model=model_name,
        openai_api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1"
    )

# Node: Tech Lead
def tech_lead_node(state: HiringCommitteeState):
    llm = get_llm()
    prompt = (
        "You are the 'Tech Lead Agent', a Senior Software Architect. You evaluate candidates with a focus on technical excellence.\n"
        "Focus: Does the candidate understand the 'why' behind the tech? Are their architectural decisions sound? How is their problem-solving logic?\n"
        "Debate Point: You prioritize technical excellence and long-term maintainability over soft skills. Be critical.\n\n"
        f"**Job Description:**\n{state['jd']}\n\n"
        f"**Resume:**\n{state['resume']}\n\n"
        f"**Screener Analysis:**\n{state['screener_analysis']}\n\n"
        "Provide your technical evaluation. Be specific about their strengths and weaknesses in their tech stack."
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"tech_lead_eval": response.content, "debate_history": [f"Tech Lead: {response.content}"]}

# Node: HR Specialist
def hr_specialist_node(state: HiringCommitteeState):
    llm = get_llm()
    prompt = (
        "You are the 'HR Specialist Agent'. You evaluate candidates for soft skills and cultural alignment.\n"
        "Focus: Teamwork, communication, conflict resolution, and core values.\n"
        "Debate Point: You prioritize 'Team Fit' and 'Burnout Risk' over pure technical prowess.\n\n"
        f"**Job Description:**\n{state['jd']}\n\n"
        f"**Resume:**\n{state['resume']}\n\n"
        f"**Tech Lead Evaluation:**\n{state['tech_lead_eval']}\n\n"
        "Provide your HR evaluation. Respond to any concerns the Tech Lead raised from a cultural perspective."
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"hr_eval": response.content, "debate_history": [f"HR Specialist: {response.content}"]}

# Node: Department Manager
def department_manager_node(state: HiringCommitteeState):
    llm = get_llm()
    prompt = (
        "You are the 'Department Manager Agent'. You look at the big picture and ROI.\n"
        "Focus: How fast can this person contribute? What is their long-term growth potential? How do they balance technical debt with business delivery?\n"
        "Debate Point: You act as the tie-breaker and decision-maker.\n\n"
        f"**Job Description:**\n{state['jd']}\n\n"
        f"**Resume:**\n{state['resume']}\n\n"
        f"**Tech Lead Evaluation:**\n{state['tech_lead_eval']}\n\n"
        f"**HR Evaluation:**\n{state['hr_eval']}\n\n"
        "Synthesize the debate. Make a final recommendation: HIRE, REJECT, or INTERVIEW_FURTHER. Justify your decision."
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"manager_decision": response.content, "debate_history": [f"Department Manager: {response.content}"]}

# Build the graph
def build_hiring_committee_graph():
    workflow = StateGraph(HiringCommitteeState)
    
    workflow.add_node("tech_lead", tech_lead_node)
    workflow.add_node("hr_specialist", hr_specialist_node)
    workflow.add_node("department_manager", department_manager_node)
    
    workflow.set_entry_point("tech_lead")
    workflow.add_edge("tech_lead", "hr_specialist")
    workflow.add_edge("hr_specialist", "department_manager")
    workflow.add_edge("department_manager", END)
    
    return workflow.compile()

def run_hiring_committee(resume: str, jd: str, screener_analysis: str):
    graph = build_hiring_committee_graph()
    initial_state = {
        "resume": resume,
        "jd": jd,
        "screener_analysis": screener_analysis,
        "tech_lead_eval": "",
        "hr_eval": "",
        "manager_decision": "",
        "debate_history": []
    }
    return graph.invoke(initial_state)
