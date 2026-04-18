import os
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"
import json
from dotenv import load_dotenv
from agents import run_screening_pipeline, run_jd_analysis, run_interview_planning_pipeline, ScreeningResult, JobRequirements, InterviewPlan
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
    print(f"{CYAN}Week 4: Linear MVP Checkpoint{RESET}\n")
    
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
        
        # FINAL UI REPORT
        print("\n" + "━"*70)
        print(f"{BOLD}{CYAN}           TALENT INTELLIGENCE REPORT - FINAL MVP{RESET}")
        print("━"*70)
        
        match_val = screen_data.match_percentage
        color = GREEN if match_val >= 80 else YELLOW if match_val >= 60 else RED
        
        print(f"{BOLD}CANDIDATE:{RESET} {candidate_name}")
        print(f"{BOLD}MATCH PROBABILITY:{RESET} {color}{match_val}%{RESET}")
        
        print(f"\n{BOLD}{GREEN}💪 KEY STRENGTHS:{RESET}")
        for s in screen_data.key_strengths:
            print(f"  ● {s}")
            
        print(f"\n{BOLD}{MAGENTA}🎯 STRATEGIC INTERVIEW QUESTIONS:{RESET}")
        for i, q in enumerate(interview_data.strategic_questions, 1):
            print(f"  {i}. {q}")
            
        print(f"\n{BOLD}{YELLOW}💡 INTERVIEWER GUIDANCE:{RESET}")
        print(f"  {interview_data.interviewer_guidance}")
            
        print("━"*70)
        rec_text = "HIRE / PROCEED" if match_val >= 75 else "REJECT"
        rec_color = GREEN if match_val >= 75 else RED
        print(f"{BOLD}{CYAN}FINAL RECOMMENDATION:{RESET} {BOLD}{rec_color}{rec_text}{RESET}")
        print("━"*70 + "\n")

    except Exception as e:
        print(f"{RED}❌ Pipeline Execution Failed: {e}{RESET}")

if __name__ == "__main__":
    main()
