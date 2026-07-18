import streamlit as st
import requests
import json

# 1. Setup Page Configurations
st.set_page_config(page_title="BabydollAI Gateway", page_icon="🎭", layout="centered")
st.title("🎭 BabydollAI: Onboarding Gateway")
st.write("Psychological preventative screening interface for high-value dating applications.")

# 2. Secure API Key Connection via UI Input
groq_api_key = st.text_input("Enter Groq API Key to Test (Free Tier):", type="password")

# 3. Define the System Prompt Engine
SYSTEM_PROMPT = """
You are a world-class forensic psychologist specializing in modern relationship dynamics, covert manipulation, and therapy-speak. 
Your job is to analyze dating app onboarding responses for subtle, modern red flags.

You MUST return a raw, valid JSON object ONLY matching this schema precisely. Do not wrap it in markdown tags or backticks:
{
  "secure_rating": 50,
  "avoidant_rating": 50,
  "toxic_risk_rating": 50,
  "justification": "Put your analysis here.",
  "status": "APPROVED"
}
"""

# 4. Building the User Interface Front-End
st.subheader("Onboarding Evaluation Question:")
user_input = st.text_area(
    "Prompt: 'What does a healthy boundary look like to you, and how do you handle it when a partner brings up a mistake you made?'",
    placeholder="Type your response here..."
)

if st.button("Submit Profile for Verification"):
    if not groq_api_key:
        st.error("Please enter a Groq API key to process.")
    elif not user_input:
        st.warning("Please input a sample text response to test.")
    else:
        with st.spinner("Analyzing linguistic psychological markers..."):
            try:
                # 5. Call Groq API via standard requests
                url = "https://groq.com"
                headers = {
                    "Authorization": f"Bearer {groq_api_key.strip()}", # Auto-cleans any accidental copied spaces
                    "Content-Type": "application/json"
                }
                data = {
                    "model": "llama-3.1-8b-instant",
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_input}
                    ],
                    "temperature": 0.2
                }
                
                response = requests.post(url, headers=headers, json=data)
                
                # Check if HTTP request failed completely
                if response.status_code != 200:
                    st.error(f"Groq API Server Error (Status {response.status_code}): {response.text}")
                else:
                    raw_content = response.json()['choices']['message']['content'].strip()
                    
                    # Strip out accidental markdown block wraps if the model inserts them
                    if raw_content.startswith("```json"):
                        raw_content = raw_content.split("```json")[1].split("```")[0].strip()
                    elif raw_content.startswith("```"):
                        raw_content = raw_content.split("```")[1].split("```")[0].strip()
                        
                    parsed_result = json.loads(raw_content)
                    
                    st.success("Analysis Complete!")
                    st.subheader("Platform Gateway Results")
                    
                    # Visual Metric Displays
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Secure Score", f"{parsed_result.get('secure_rating', 0)}%")
                    col2.metric("Avoidant Score", f"{parsed_result.get('avoidant_rating', 0)}%")
                    col3.metric("Toxic Risk Score", f"{parsed_result.get('toxic_risk_rating', 0)}%")
                    
                    st.info(f"**Gatekeeper Status:** {parsed_result.get('status', 'PENDING')}")
                    st.write(f"**Psychological Rationale:** {parsed_result.get('justification', 'No justification provided.')}")
                
            except Exception as e:
                st.error(f"An internal error occurred while parsing the AI data: {e}")
