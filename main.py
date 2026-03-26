import os
import json
from dotenv import load_dotenv
from agents.screener_agent import run_screening_pipeline, ScreeningResult
from agents.utils import parse_pdf, read_text_file

# Load environment variables
load_dotenv()

def parse_result(result):
    """Parse CrewAI result into ScreeningResult, handling multiple output formats."""
    # Try pydantic first (works with OpenAI native)
    if result.pydantic:
        return result.pydantic
    
    # Try json_dict (works with some providers)
    if result.json_dict:
        return ScreeningResult(**result.json_dict)
    
    # Fallback: parse the raw string output as JSON
    raw = str(result.raw) if hasattr(result, 'raw') else str(result)
    # Find JSON in the output (might be wrapped in markdown code blocks)
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return ScreeningResult(**json.loads(raw))

def main():
    print("🚀 Welcome to TalentStream AI - Week 1: Screener Demo\n")
    
    # Check for API Key
    if not os.getenv("GROQ_API_KEY"):
        print("❌ Error: GROQ_API_KEY not found in environment variables.")
        print("Please create a .env file with your Groq API key.")
        print("Get a free key at: https://console.groq.com/keys")
        return

    # User Inputs (for Demo)
    jd_path = "data/Samples/jd_senior_fs.txt"
    resume_path = "data/Samples/resume_jane_doe.txt"
    
    print(f"📄 Parsing Job Description from: {jd_path}")
    jd_text = read_text_file(jd_path)
    
    print(f"📄 Parsing Resume from: {resume_path}")
    # Handle both .txt and .pdf for the demo
    if resume_path.endswith(".pdf"):
        resume_text = parse_pdf(resume_path)
    else:
        resume_text = read_text_file(resume_path)
    
    if not jd_text or not resume_text:
        print("❌ Error: Could not read Job Description or Resume.")
        return

    print("\n🔍 Running Screener Agent Pipeline...")
    try:
        result = run_screening_pipeline(jd_text, resume_text)
        screening_data = parse_result(result)
        
        print("\n" + "="*50)
        print("✅ SCREENING RESULTS")
        print("="*50)
        print(f"🔥 Match Percentage: {screening_data.match_percentage}%")
        print(f"\n📝 Candidate Summary: {screening_data.candidate_summary}")
        
        print("\n💪 Key Strengths:")
        for strength in screening_data.key_strengths:
            print(f"  - {strength}")
            
        print("\n⚠️ Missing Skills:")
        for skill in screening_data.missing_skills:
            print(f"  - {skill}")
            
        print("\n🕵️ Areas to Probe (Interview Questions):")
        for probe in screening_data.areas_to_probe:
            print(f"  - {probe}")
        print("="*50)

    except Exception as e:
        print(f"❌ Error during pipeline execution: {e}")

if __name__ == "__main__":
    main()
