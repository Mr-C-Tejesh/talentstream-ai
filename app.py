import streamlit as st
import requests
import json
import os
from pypdf import PdfReader
from io import BytesIO

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="TalentStream AI | Recruiter Dashboard",
    page_icon="🤖",
    layout="wide"
)

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    /* Main container styling */
    .stApp {
        background-color: var(--background-color);
    }
    
    /* Custom Button Styling */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3.5em;
        background: linear-gradient(135deg, #007bff, #00d4ff);
        color: white !important;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,123,255,0.3);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,123,255,0.4);
    }
    
    /* Agent Card Glassmorphism */
    .agent-card {
        padding: 24px;
        border-radius: 12px;
        background-color: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.1);
        border-left: 6px solid #007bff;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        color: var(--text-color);
        line-height: 1.6;
    }
    
    /* Agent Specific Accents */
    .tech-lead { border-left-color: #ffc107; background-image: linear-gradient(to right, rgba(255, 193, 7, 0.05), transparent); }
    .hr-spec { border-left-color: #e83e8c; background-image: linear-gradient(to right, rgba(232, 62, 140, 0.05), transparent); }
    .manager { border-left-color: #17a2b8; background-image: linear-gradient(to right, rgba(23, 162, 184, 0.05), transparent); }
    
    /* Header styling */
    h1, h2, h3 {
        color: var(--text-color);
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: var(--secondary-background-color);
        border-right: 1px solid rgba(128, 128, 128, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.title("⚙️ TalentStream AI")
st.sidebar.markdown("---")
api_url = st.sidebar.text_input("API Base URL", value="http://localhost:8000")
st.sidebar.info("This dashboard connects to the TalentStream AI FastAPI backend to run autonomous multi-agent hiring workflows.")

# --- HELPERS ---
def get_resume_text(uploaded_file):
    try:
        if uploaded_file.name.lower().endswith('.pdf'):
            pdf = PdfReader(uploaded_file)
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        else:
            return uploaded_file.getvalue().decode("utf-8")
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
        return None

# --- SESSION STATE ---
if 'results' not in st.session_state:
    st.session_state.results = None

# --- MAIN UI ---
st.title("🚀 TalentStream AI Dashboard")
st.subheader("Autonomous Multi-Agent Hiring & Interviewing Engine")

tab1, tab2, tab3, tab4 = st.tabs(["📄 Upload & Analyze", "🏛️ Hiring Committee", "📊 Talent Intelligence Report", "🎤 Simulated Interview"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 1. Job Description")
        jd_text = st.text_area("Paste the Job Description here...", height=300, 
                               placeholder="We are looking for a Senior Full-Stack Engineer...")
        
    with col2:
        st.markdown("### 2. Candidate Resume")
        uploaded_file = st.file_uploader("Upload Resume (PDF or TXT)", type=["pdf","txt"])
        candidate_name = st.text_input("Candidate Name", placeholder="e.g. Jane Doe")

    if st.button("🔥 Run End-to-End Evaluation"):
        if not jd_text or not uploaded_file or not candidate_name:
            st.error("Please provide JD, Resume, and Candidate Name.")
        else:
            with st.spinner("🕵️ Agents are collaborating... this takes about 60-90 seconds."):
                # 1. Extract Text
                resume_text = get_resume_text(uploaded_file)
                
                if resume_text:
                    try:
                        payload = {
                            "candidate_name": candidate_name,
                            "jd_text": jd_text,
                            "resume_text": resume_text
                        }
                        
                        # 2. Call Backend
                        response = requests.post(f"{api_url}/evaluate-candidate", json=payload, timeout=300)
                        
                        if response.status_code == 200:
                            st.session_state.results = response.json()
                            st.success("✅ Evaluation Complete!")
                            st.balloons()
                        else:
                            st.error(f"❌ Backend Error ({response.status_code}): {response.text}")
                    except requests.exceptions.ConnectionError:
                        st.error(f"❌ Failed to connect to backend at {api_url}. Is the FastAPI server running?")
                    except Exception as e:
                        st.error(f"❌ Unexpected Error: {e}")

with tab2:
    if st.session_state.results:
        st.markdown("### 🏛️ The Hiring Committee Debate")
        st.info("The agents below used LangGraph to debate the candidate's fit in multiple cycles.")
        
        debate = st.session_state.results.get('committee_debate', {})
        history = debate.get('debate_history', [])
        
        if history:
            for entry in history:
                if "Tech Lead" in entry:
                    with st.container():
                        st.markdown(f"""<div class="agent-card tech-lead">
                        <strong>👨‍💻 Tech Lead Evaluation</strong><br>{entry.split(':', 1)[1]}
                        </div>""", unsafe_allow_html=True)
                elif "HR Specialist" in entry:
                    with st.container():
                        st.markdown(f"""<div class="agent-card hr-spec">
                        <strong>🤝 HR Specialist Evaluation</strong><br>{entry.split(':', 1)[1]}
                        </div>""", unsafe_allow_html=True)
                elif "Manager" in entry:
                    with st.container():
                        st.markdown(f"""<div class="agent-card manager">
                        <strong>🏢 Department Manager Decision</strong><br>{entry.split(':', 1)[1]}
                        </div>""", unsafe_allow_html=True)
        else:
            st.warning("No debate logs found.")
    else:
        st.write("Run an evaluation first to see the debate.")

with tab3:
    if st.session_state.results:
        res = st.session_state.results
        
        st.markdown(f"## Talent Report: {candidate_name}")
        
        m_col1, m_col2 = st.columns(2)
        match_val = res['screening']['match_percentage']
        m_col1.metric("Match Score", f"{match_val}%")
        
        decision = "HIRE" if match_val > 75 else "REJECT"
        m_col2.metric("Recommendation", decision)

        st.markdown("### 💪 Key Strengths")
        for s in res['screening']['key_strengths']:
            st.markdown(f"- {s}")

        st.markdown("### 🎯 Strategic Interview Questions")
        for i, q in enumerate(res['interview_plan']['strategic_questions'], 1):
            st.info(f"**Question {i}:** {q}")
            
        with st.expander("🔍 View Raw Screener Analysis"):
            st.json(res['screening'])
            
        with st.expander("🧠 View Extracted JD Requirements"):
            st.json(res['requirements'])
    else:
        st.write("Run an evaluation first to generate the report.")

with tab4:
    st.markdown("### 🎤 Simulated Interview Practice")
    st.info("Practice answering the strategic questions generated by the Interviewer Agent.")
    
    if st.session_state.results:
        res = st.session_state.results
        questions = res['interview_plan']['strategic_questions']
        
        selected_question = st.selectbox("Select a question to practice:", questions)
        
        candidate_answer = st.text_area("Your Answer:", height=150, placeholder="Type your answer here as if you were in the interview...")
        
        if st.button("Submit Answer for Feedback"):
            if not candidate_answer:
                st.warning("Please provide an answer first.")
            else:
                with st.spinner("The Interviewer is evaluating your answer..."):
                    try:
                        context = f"Candidate Summary: {res['screening']['candidate_summary']}\nRole: {res['requirements']['role_title']}"
                        payload = {
                            "question": selected_question,
                            "candidate_answer": candidate_answer,
                            "context": context
                        }
                        
                        response = requests.post(f"{api_url}/mock-interview-reply", json=payload, timeout=60)
                        
                        if response.status_code == 200:
                            feedback = response.json().get("feedback", "")
                            st.markdown("#### 🤖 Interviewer Feedback")
                            st.markdown(f"> {feedback}")
                        else:
                            st.error(f"❌ Backend Error ({response.status_code}): {response.text}")
                    except Exception as e:
                        st.error(f"❌ Failed to connect to backend: {e}")
    else:
        st.write("Run an evaluation first to generate interview questions.")
