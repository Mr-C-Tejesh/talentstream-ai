import os
from dotenv import load_dotenv
from agents.jd_analyzer_agent import run_jd_analysis, JobRequirements
from agents.sourcing_agent import run_sourcing_pipeline, SourcingResults
from agents.utils import read_text_file, parse_agent_output

# Load environment variables
load_dotenv()

def main():
    print("🔍 TalentStream AI - Sourcing Agent Test")
    
    # 1. Read a Sample JD
    jd_path = "data/Samples/jd_senior_fs.txt"
    jd_text = read_text_file(jd_path)
    
    if not jd_text:
        print("❌ Error: Could not read Job Description.")
        return

    try:
        # 2. Analyze the JD first (to get structured requirements)
        print("\n🧠 Step 1: Analyzing Job Description...")
        jd_result = run_jd_analysis(jd_text)
        jd_requirements = parse_agent_output(jd_result, JobRequirements)
        print(f"✅ Target Role: {jd_requirements.role_title}")

        # 3. Run Sourcing Agent
        print("\n🕵️ Step 2: Sourcing candidates from Vector DB...")
        sourcing_result = run_sourcing_pipeline(jd_requirements)
        data = parse_agent_output(sourcing_result, SourcingResults)

        # 4. Display Results
        print("\n" + "="*60)
        print(f"🎯 TOP CANDIDATES FOUND FOR: {jd_requirements.role_title}")
        print("="*60)

        if not data.top_candidates:
            print("No matching candidates found in the database.")
        else:
            for i, candidate in enumerate(data.top_candidates, 1):
                print(f"\n{i}. {candidate.name}")
                print(f"   Similarity Score: {candidate.score:.2f}")
                print(f"   Headhunter Reasoning: {candidate.match_reasoning}")
        
        print("\n" + "="*60)

    except Exception as e:
        print(f"❌ Error during sourcing test: {e}")

if __name__ == "__main__":
    main()
