import os
from dotenv import load_dotenv
from agents.vector_db import VectorDB
from agents.utils import parse_pdf, read_text_file

# Load environment variables
load_dotenv()

def main():
    print("🚀 TalentStream AI - Resume Ingestion Utility")
    db = VectorDB()
    
    # 1. Initialize DB tables (Resetting to handle dimension change to 384)
    if not db.initialize_db(reset=True):
        print("❌ Could not initialize database. Check your DATABASE_URL.")
        return

    # 2. Process sample files
    samples_dir = "data/Samples"
    for filename in os.listdir(samples_dir):
        if filename.startswith("resume_"):
            filepath = os.path.join(samples_dir, filename)
            print(f"📄 Processing: {filename}...")
            
            try:
                # Extract candidate name from filename (e.g., resume_john_smith.txt -> John Smith)
                name = filename.replace("resume_", "").split(".")[0].replace("_", " ").title()
                
                # Parse text
                if filename.endswith(".pdf"):
                    text = parse_pdf(filepath)
                else:
                    text = read_text_file(filepath)
                
                if text:
                    db.add_resume(name, text, {"source": "Samples", "filename": filename})
                else:
                    print(f"⚠️ Could not extract text from {filename}")
                    
            except Exception as e:
                print(f"❌ Error processing {filename}: {e}")

    print("\n✅ Ingestion complete.")

if __name__ == "__main__":
    main()
