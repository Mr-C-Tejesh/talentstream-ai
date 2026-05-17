import os
from typing import List, Dict, TypedDict, Annotated, Union, Literal
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
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
    num_rounds: int
    human_input: str
    consensus_reached: bool

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
    rounds_context = f"This is debate round {state.get('num_rounds', 0) + 1}."
    human_context = f"\n**Human Recruiter Nudge:** {state.get('human_input', 'None')}" if state.get('human_input') else ""
    
    prompt = (
        "You are the 'Tech Lead Agent', a Senior Software Architect. You evaluate candidates with a focus on technical excellence.\n"
        f"{rounds_context}\n"
        "Focus: Does the candidate understand the 'why' behind the tech? Are their architectural decisions sound?\n"
        "Debate Point: You prioritize technical excellence. Be critical. If this is a subsequent round, respond to the HR Specialist's or Manager's comments.\n"
        f"{human_context}\n\n"
        f"**Job Description:**\n{state['jd']}\n\n"
        f"**Resume:**\n{state['resume']}\n\n"
        f"**Screener Analysis:**\n{state['screener_analysis']}\n\n"
        f"**Current Debate History:**\n" + "\n".join(state['debate_history']) + "\n\n"
        "Provide your evaluation update."
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    history = state.get('debate_history', [])
    history.append(f"Round {state.get('num_rounds', 0) + 1} - Tech Lead: {response.content}")
    return {
        "tech_lead_eval": response.content, 
        "debate_history": history,
        "num_rounds": state.get('num_rounds', 0) + 1
    }

# Node: HR Specialist
def hr_specialist_node(state: HiringCommitteeState):
    llm = get_llm()
    prompt = (
        "You are the 'HR Specialist Agent'. You evaluate candidates for soft skills and cultural alignment.\n"
        "Focus: Teamwork, communication, conflict resolution, and core values.\n"
        "Debate Point: You prioritize 'Team Fit' over pure technical prowess. Respond to the Tech Lead's concerns.\n\n"
        f"**Job Description:**\n{state['jd']}\n\n"
        f"**Resume:**\n{state['resume']}\n\n"
        f"**Current Debate History:**\n" + "\n".join(state['debate_history']) + "\n\n"
        "Provide your HR evaluation update."
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    history = state.get('debate_history', [])
    history.append(f"Round {state.get('num_rounds', 0)} - HR Specialist: {response.content}")
    return {"hr_eval": response.content, "debate_history": history}

# Node: Department Manager (Decision Node)
def department_manager_node(state: HiringCommitteeState):
    llm = get_llm()
    
    # Check for consensus or need for more rounds
    decision_prompt = (
        "You are the 'Department Manager Agent'. You act as the tie-breaker and decision-maker.\n"
        "Review the debate history. Is there a clear consensus or do you need the agents to clarify further?\n"
        "If you have enough info, provide a final decision (HIRE/REJECT/INTERVIEW). If you need more debate, state what needs clarification.\n\n"
        f"**Debate History:**\n" + "\n".join(state['debate_history']) + "\n\n"
        "Output your final synthesis and decision. Start your response with 'CONSENSUS_REACHED: TRUE' if you are done, or 'CONSENSUS_REACHED: FALSE' if you want another round of debate."
    )
    response = llm.invoke([HumanMessage(content=decision_prompt)])
    
    consensus = "CONSENSUS_REACHED: TRUE" in response.content.upper()
    history = state.get('debate_history', [])
    history.append(f"Round {state.get('num_rounds', 0)} - Manager: {response.content}")
    
    return {
        "manager_decision": response.content, 
        "debate_history": history,
        "consensus_reached": consensus
    }

# Conditional logic for the loop
def should_continue(state: HiringCommitteeState) -> Literal["tech_lead", END]:
    if state.get("consensus_reached") or state.get("num_rounds", 0) >= 3:
        return END
    return "tech_lead"

# Build the graph
def build_hiring_committee_graph():
    workflow = StateGraph(HiringCommitteeState)
    
    workflow.add_node("tech_lead", tech_lead_node)
    workflow.add_node("hr_specialist", hr_specialist_node)
    workflow.add_node("department_manager", department_manager_node)
    
    workflow.set_entry_point("tech_lead")
    workflow.add_edge("tech_lead", "hr_specialist")
    workflow.add_edge("hr_specialist", "department_manager")
    
    # Cyclic edge based on manager's decision
    workflow.add_conditional_edges(
        "department_manager",
        should_continue,
        {
            "tech_lead": "tech_lead",
            END: END
        }
    )
    
    # Add checkpointer for state persistence
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory, interrupt_before=["tech_lead"] if False else []) # HITL handling

def run_hiring_committee(resume: str, jd: str, screener_analysis: str, thread_id: str = "1"):
    graph = build_hiring_committee_graph()
    
    config = {"configurable": {"thread_id": thread_id}}
    
    initial_state = {
        "resume": resume,
        "jd": jd,
        "screener_analysis": screener_analysis,
        "tech_lead_eval": "",
        "hr_eval": "",
        "manager_decision": "",
        "debate_history": [],
        "num_rounds": 0,
        "human_input": "",
        "consensus_reached": False
    }
    
    return graph.invoke(initial_state, config=config)
