import os
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"
import json
from dotenv import load_dotenv
from agents import run_screening_pipeline, run_jd_analysis, run_interview_planning_pipeline, ScreeningResult, JobRequirements, InterviewPlan
from agents.hiring_committee import run_hiring_committee
from agents.utils import parse_pdf, read_text_file, parse_agent_output

# ANSI Color Codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

# Load environment variables
load_dotenv()

def main():
    print(f"\n{BOLD}{CYAN}TalentStream AI{RESET} - {BOLD}Autonomous Multi-Agent Hiring System{RESET}")
    print(f"{CYAN}Week 5: Agentic Shift (LangGraph Committee Debate){RESET}\n")
    
    if not os.getenv("GROQ_API_KEY"):
        print(f"{RED}❌ Error: GROQ_API_KEY not found.{RESET}")
        return

    # User Inputs (Demo Mode)
    jd_path = "data/Samples/jd_senior_fs.txt"
    resume_path = "data/Samples/resume_jane_doe.txt"
    candidate_name = "Jane Doe"
    
    print(f"📄 {BOLD}Reading Requirements...{RESET}")
    jd_text = read_text_file(jd_path)
    resume_text = read_text_file(resume_path)
    
    if not jd_text or not resume_text:
        print(f"{RED}❌ Error: Files not found.{RESET}")
        return

    try:
        # STEP 1: JD Analysis
        print(f"\n{YELLOW}🧠 Step 1: Agentic JD Analysis...{RESET}")
        jd_result = run_jd_analysis(jd_text)
        jd_requirements = parse_agent_output(jd_result, JobRequirements)
        print(f"{GREEN}✅ JD Analyzed: {BOLD}{jd_requirements.role_title}{RESET}")

        # STEP 2: Candidate Screening
        print(f"\n{YELLOW}🔍 Step 2: Technical Screening...{RESET}")
        screen_result = run_screening_pipeline(jd_requirements, resume_text)
        screen_data = parse_agent_output(screen_result, ScreeningResult)
        print(f"{GREEN}✅ Screening Complete: {BOLD}{screen_data.match_percentage}% Match{RESET}")

        # STEP 3: Interview Planning
        print(f"\n{YELLOW}📋 Step 3: Generating Strategic Interview Plan...{RESET}")
        interview_result = run_interview_planning_pipeline(candidate_name, jd_requirements, screen_data)
        interview_data = parse_agent_output(interview_result, InterviewPlan)
        print(f"{GREEN}✅ Interview Plan Generated.{RESET}")

        # STEP 4: Hiring Committee Debate (Week 5 Feature)
        print(f"\n{MAGENTA}🏛️  Step 4: Convening the Hiring Committee (LangGraph Debate)...{RESET}")
        screener_summary = screen_data.candidate_summary + "\nStrengths: " + ", ".join(screen_data.key_strengths)
        
        committee_result = run_hiring_committee(
            resume=resume_text,
            jd=jd_text,
            screener_analysis=screener_summary
        )

        # FINAL UI REPORT
        print("\n" + "━"*80)
        print(f"{BOLD}{CYAN}           TALENT INTELLIGENCE REPORT - FINAL HI-TECH EDITION{RESET}")
        print("━"*80)
        
        match_val = screen_data.match_percentage
        color = GREEN if match_val >= 80 else YELLOW if match_val >= 60 else RED
        
        print(f"{BOLD}CANDIDATE:{RESET} {candidate_name}")
        print(f"{BOLD}MATCH PROBABILITY:{RESET} {color}{match_val}%{RESET}")
        
        print(f"\n{BOLD}{GREEN}💪 KEY STRENGTHS:{RESET}")
        for s in screen_data.key_strengths:
            print(f"  ● {s}")
            
        print(f"\n{BOLD}{YELLOW}👨‍💻 TECH LEAD EVALUATION:{RESET}")
        print(f"{committee_result['tech_lead_eval'].strip()[:500]}...") # Truncated for UI
        
        print(f"\n{BOLD}{MAGENTA}🤝 HR SPECIALIST EVALUATION:{RESET}")
        print(f"{committee_result['hr_eval'].strip()[:500]}...") # Truncated for UI
        
        print(f"\n{BOLD}{CYAN}🏢 DEPARTMENT MANAGER FINAL DECISION:{RESET}")
        print(f"{committee_result['manager_decision'].strip()}")
            
        print("━"*80)
        print(f"{BOLD}{CYAN}TalentStream AI: Engineering Success through Collaboration.{RESET}")
        print("━"*80 + "\n")

    except Exception as e:
        print(f"{RED}❌ Pipeline Execution Failed: {e}{RESET}")

if __name__ == "__main__":
    main()
