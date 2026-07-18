import streamlit as st
from groq import Groq
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

You MUST return a raw, valid JSON object ONLY matching this schema precisely. Do not wrap it in markdown text blocks:
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
                # 5. Initialize the Official Groq Client
                client = Groq(api_key=groq_api_key.strip())
                
                # 6. Call the Completion Request
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    response_format={"type": "json_object"},
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_input}
                    ],
                    temperature=0.2
                )
                
                # 7. Extract and Render Output
                raw_content = response.choices[0].message.content.strip()
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
                st.error(f"An error occurred while calling the server: {e}")
