# TalentStream AI 🚀
import os
import json
from dotenv import load_dotenv
from agents.screener_agent import run_screening_pipeline, ScreeningResult
from agents.utils import parse_pdf, read_text_file

# ANSI Color Codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
CYAN = "\033[96m"
RESET = "\033[0m"

# Load environment variables
load_dotenv()

def parse_result(result):
    """Parse CrewAI result into ScreeningResult, handling multiple output formats."""
    # Try pydantic first (works with OpenAI native)
    if hasattr(result, 'pydantic') and result.pydantic:
        return result.pydantic
    
    # Try json_dict (works with some providers)
    if hasattr(result, 'json_dict') and result.json_dict:
        return ScreeningResult(**result.json_dict)
    
    # Fallback: parse the raw string output as JSON
    raw = str(result.raw) if hasattr(result, 'raw') else str(result)
    # Find JSON in the output (might be wrapped in markdown code blocks)
    raw = raw.strip()
    if raw.startswith("```"):
        # Remove markdown wrapper
        lines = raw.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines[-1].strip() == "```":
            lines = lines[:-1]
        raw = "\n".join(lines).strip()
    
    return ScreeningResult(**json.loads(raw))

def main():
    print(f"\n{BOLD}{CYAN}TalentStream AI{RESET} - {BOLD}Autonomous Multi-Agent Hiring System{RESET}")
    print(f"{CYAN}Week 1: Digital Screener Demo{RESET}\n")
    
    # Check for API Key
    if not os.getenv("GROQ_API_KEY"):
        print(f"{RED}❌ Error: GROQ_API_KEY not found in environment variables.{RESET}")
        print("Please create a .env file with your Groq API key.")
        print("Get a free key at: https://console.groq.com/keys")
        return

    # User Inputs (for Demo)
    jd_path = "data/Samples/jd_senior_fs.txt"
    resume_path = "data/Samples/resume_jane_doe.txt"
    
    print(f"📄 {BOLD}Reading Job Description:{RESET} {jd_path}")
    jd_text = read_text_file(jd_path)
    
    print(f"📄 {BOLD}Reading Resume:{RESET} {resume_path}")
    # Handle both .txt and .pdf for the demo
    if resume_path.endswith(".pdf"):
        resume_text = parse_pdf(resume_path)
    else:
        resume_text = read_text_file(resume_path)
    
    if not jd_text or not resume_text:
        print(f"{RED}❌ Error: Could not read Job Description or Resume.{RESET}")
        return

    print(f"\n{YELLOW}🔍 Orchestrating Agents... (This may take a moment){RESET}")
    try:
        result = run_screening_pipeline(jd_text, resume_text)
        data = parse_result(result)
        
        # Determine Color for Match Percentage
        match_val = data.match_percentage
        color = GREEN if match_val >= 80 else YELLOW if match_val >= 60 else RED
        
        print("\n" + "━"*60)
        print(f"{BOLD}{CYAN}           TALENT INTELLIGENCE REPORT - SCREENER{RESET}")
        print("━"*60)
        
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
