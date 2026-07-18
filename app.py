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

You MUST return a raw JSON object ONLY matching this schema precisely. Do not include markdown or text wrapping:
{
  "secure_rating": 0,
  "avoidant_rating": 0,
  "toxic_risk_rating": 0,
  "justification": "2-sentence psychological rationale.",
  "status": "APPROVED or REJECTED"
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
                # 5. Call Groq API via standard requests (Free Llama 3 Model)
                url = "https://groq.com"
                headers = {
                    "Authorization": f"Bearer {groq_api_key}",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": "llama3-8b-8192",
                    "response_format": {"type": "json_object"},
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_input}
                    ]
                }
                
                response = requests.post(url, headers=headers, json=data)
                result_json = response.json()['choices'][0]['message']['content']
                parsed_result = json.loads(result_json)
                
                st.success("Analysis Complete!")
                st.subheader("Platform Gateway Results")
                
                # Visual Metric Displays
                col1, col2, col3 = st.columns(3)
                col1.metric("Secure Score", f"{parsed_result['secure_rating']}%")
                col2.metric("Avoidant Score", f"{parsed_result['avoidant_rating']}%")
                col3.metric("Toxic Risk Score", f"{parsed_result['toxic_risk_rating']}%")
                
                st.info(f"**Gatekeeper Status:** {parsed_result['status']}")
                st.write(f"**Psychological Rationale:** {parsed_result['justification']}")
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
