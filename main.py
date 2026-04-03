# TalentStream AI 🚀
import os
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"
import json
from dotenv import load_dotenv
from agents import run_screening_pipeline, run_jd_analysis, ScreeningResult, JobRequirements
from agents.utils import parse_pdf, read_text_file, parse_agent_output

# ANSI Color Codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
CYAN = "\033[96m"
RESET = "\033[0m"

# Load environment variables
load_dotenv()

def main():
    print(f"\n{BOLD}{CYAN}TalentStream AI{RESET} - {BOLD}Autonomous Multi-Agent Hiring System{RESET}")
    print(f"{CYAN}Week 2: Multi-Agent Digital Screener & API{RESET}\n")
    
    if not os.getenv("GROQ_API_KEY"):
        print(f"{RED}❌ Error: GROQ_API_KEY not found.{RESET}")
        return

    # User Inputs
    jd_path = "data/Samples/jd_senior_fs.txt"
    resume_path = "data/Samples/resume_jane_doe.txt"
    
    print(f"📄 {BOLD}Reading Files...{RESET}")
    jd_text = read_text_file(jd_path)
    resume_text = parse_pdf(resume_path) if resume_path.endswith(".pdf") else read_text_file(resume_path)
    
    if not jd_text or not resume_text:
        print(f"{RED}❌ Error: Files not found.{RESET}")
        return

    try:
        # STEP 1: JD Analysis
        print(f"\n{YELLOW}🧠 Step 1: Analyzing Job Description...{RESET}")
        jd_result = run_jd_analysis(jd_text)
        jd_requirements = parse_agent_output(jd_result, JobRequirements)
        
        print(f"{GREEN}✅ JD Analyzed: {BOLD}{jd_requirements.role_title}{RESET}")
        print(f"   Required Tech: {', '.join(jd_requirements.required_tech_stack[:5])}...")

        # STEP 2: Candidate Screening
        print(f"\n{YELLOW}🔍 Step 2: Orchestrating Screener Agent...{RESET}")
        screen_result = run_screening_pipeline(jd_requirements, resume_text)
        data = parse_agent_output(screen_result, ScreeningResult)
        
        # UI Report
        match_val = data.match_percentage
        color = GREEN if match_val >= 80 else YELLOW if match_val >= 60 else RED
        
        print("\n" + "━"*60)
        print(f"{BOLD}{CYAN}           TALENT INTELLIGENCE REPORT - SCREENER{RESET}")
        print("━"*60)
        
        print(f"{BOLD}ROLE:{RESET} {jd_requirements.role_title}")
        print(f"{BOLD}MATCH PROBABILITY:{RESET} {color}{match_val}%{RESET}")
        print(f"\n{BOLD}CANDIDATE SUMMARY:{RESET}\n{data.candidate_summary}")
        
        print(f"\n{BOLD}{GREEN}💪 CORE STRENGTHS:{RESET}")
        for strength in data.key_strengths:
            print(f"  ● {strength}")
            
        print(f"\n{BOLD}{RED}❌ CRITICAL GAPS:{RESET}")
        for skill in data.missing_skills:
            print(f"  ○ {skill}")
            
        print(f"\n{BOLD}{YELLOW}🕵️ INTERVIEW PROBE AREAS:{RESET}")
        for i, probe in enumerate(data.areas_to_probe, 1):
            print(f"  {i}. {probe}")
            
        print("━"*60)
        rec_color = GREEN if match_val >= 70 else RED
        rec_text = "PROCEED TO INTERVIEW" if match_val >= 70 else "REJECT"
        print(f"{BOLD}{CYAN}RECOMMENDATION:{RESET} {BOLD}{rec_color}{rec_text}{RESET}")
        print("━"*60 + "\n")

    except Exception as e:
        print(f"{RED}❌ Pipeline Execution Failed: {e}{RESET}")

if __name__ == "__main__":
    main()
