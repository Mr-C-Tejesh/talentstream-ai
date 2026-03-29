import os
import json
from dotenv import load_dotenv
from agents.jd_analyzer_agent import run_jd_analysis, JobRequirements
from agents.utils import read_text_file

# Load environment variables
load_dotenv()

def parse_result(result):
    """Parse CrewAI result into JobRequirements, handling multiple output formats."""
    # Try pydantic first (works with OpenAI native)
    if hasattr(result, 'pydantic') and result.pydantic:
        return result.pydantic
    
    # Try json_dict (works with some providers)
    if hasattr(result, 'json_dict') and result.json_dict:
        return JobRequirements(**result.json_dict)
    
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
    
    return JobRequirements(**json.loads(raw))

def main():
    print("Testing JD Analyzer Agent...")
    
    jd_path = "data/Samples/jd_senior_fs.txt"
    jd_text = read_text_file(jd_path)
    
    if not jd_text:
        print("Error: Could not read Job Description.")
        return

    print("Analyzing JD...")
    try:
        result = run_jd_analysis(jd_text)
        data = parse_result(result)
        
        print("\n" + "="*50)
        print(f"ROLE: {data.role_title}")
        print(f"MIN EXPERIENCE: {data.min_years_experience} years")
        print("="*50)
        
        print("\nCORE TECH STACK:")
        for tech in data.required_tech_stack:
            print(f"- {tech}")
            
        print("\nMUST-HAVES:")
        for must in data.must_haves:
            print(f"- {must}")
            
        print("\nSOFT SKILLS:")
        for skill in data.soft_skills:
            print(f"- {skill}")
            
        print("\nPREFERRED:")
        for pref in data.preferred_qualifications:
            print(f"- {pref}")
            
    except Exception as e:
        print(f"Error during JD Analysis: {e}")

if __name__ == "__main__":
    main()
