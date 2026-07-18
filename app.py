import streamlit as st
from groq import Groq
import json

# 1. Setup Page Configurations
st.set_page_config(page_title="BabydollAI Gateway", page_icon="🎭", layout="centered")
st.title("🎭 BabydollAI: Premium Onboarding Gateway")
st.write("Advanced behavioral screening infrastructure to detect weaponized therapy-speak and covert manipulation.")

# 2. Secure API Key Connection via UI Input
groq_api_key = "PASTE_YOUR_ACTUAL_GSK_KEY_HERE"


# 3. Define the System Prompt Engine (Strict Forensic Mode with Advanced Output)
SYSTEM_PROMPT = """
You are a cynical, world-class forensic psychologist screening for covert narcissism, weaponized therapy-speak, and emotional unavailability. 
Do not be fooled by wellness buzzwords. If a user uses psychology terms to evade accountability, punish them heavily.

You MUST return a raw, valid JSON object ONLY matching this schema precisely. Do not include markdown tags:
{
  "secure_rating": 10,
  "avoidant_rating": 85,
  "toxic_risk_rating": 80,
  "deception_score": 90,
  "flagged_keywords": ["protecting my peace", "unresolved trauma"],
  "justification": "Expose the exact therapy-speak words they used to deflect accountability.",
  "secure_translation": "How a truly secure person would phrase this cleanly.",
  "status": "REJECTED"
}
"""

# 4. Building the User Interface Front-End
st.subheader("Onboarding Evaluation Question:")
user_input = st.text_area(
    "Prompt: 'What does a healthy boundary look like to you, and how do you handle it when a partner brings up a mistake you made?'",
    placeholder="Type your response here..."
)

if st.button("Submit Profile for Deep Behavioral Analysis"):
   if st.button("Submit Profile for Deep Behavioral Analysis"):
    if not user_input:

        st.warning("Please input a sample text response to test.")
    else:
        with st.spinner("Executing forensic linguistic analysis..."):
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
                
                # Visual Metric Displays (Row 1)
                col1, col2, col3 = st.columns(3)
                col1.metric("Secure Score", f"{parsed_result.get('secure_rating', 0)}%")
                col2.metric("Avoidant Score", f"{parsed_result.get('avoidant_rating', 0)}%")
                col3.metric("Toxic Risk Score", f"{parsed_result.get('toxic_risk_rating', 0)}%")
                
                # Advanced Metric (Row 2)
                st.write("### 🚨 Covert Manipulation Profile")
                st.progress(parsed_result.get('deception_score', 0) / 100)
                st.caption(f"**Deception & Camouflage Meter:** {parsed_result.get('deception_score', 0)}% use of weaponized therapy buzzwords.")
                
                # Flagged Keywords UI
                keywords = parsed_result.get('flagged_keywords', [])
                if keywords:
                    st.write("**Weaponized Terms Detected:**")
                    st.write(" , ".join([f"`{kw}`" for kw in keywords]))
                
                # Rationale & Status
                st.info(f"**Gatekeeper Decision:** {parsed_result.get('status', 'PENDING')}")
                st.write(f"**Psychological Rationale:** {parsed_result.get('justification', 'No analysis generated.')}")
                
                # Secure Translation Feature
                st.subheader("💡 Secure Alignment Prescription")
                st.success(f"**How a Secure Partner Communicates:** *\"{parsed_result.get('secure_translation', 'No translation generated.')}\"*")
                
            except Exception as e:
                st.error(f"An error occurred while calling the server: {e}")
