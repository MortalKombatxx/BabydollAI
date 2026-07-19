import streamlit as st
import os
import json

# 1. Setup Page Configurations
st.set_page_config(page_title="BabydollAI Gateway", page_icon="🎭", layout="centered")
st.title("🎭 BabydollAI: Enterprise Onboarding Gateway")
st.write("Forensic behavioral screening middleware engineered via OpenAI Codex and GPT-5.6 infrastructure.")

# 2. Secure Token Inputs
st.sidebar.header("🔑 Authentication Framework")
provider = st.sidebar.selectbox("Select Inference Backbone:", ["OpenAI GPT-5.6 (Official)", "Groq Llama-3.1 (Fallback Free Tier)"])
api_key = st.sidebar.text_input("Enter Chosen Provider API Key:", type="password")

# 3. Define System Prompt
SYSTEM_PROMPT = """
You are a cynical, world-class forensic psychologist screening for covert narcissism, weaponized therapy-speak, and emotional unavailability. 
You MUST return a raw, valid JSON object ONLY matching this schema precisely. No markdown block wraps:
{
  "secure_rating": 10,
  "avoidant_rating": 85,
  "toxic_risk_rating": 80,
  "deception_score": 95,
  "flagged_keywords": ["protecting my peace"],
  "justification": "Expose the exact therapy-speak words they used to deflect accountability.",
  "secure_translation": "How a truly secure partner communicates.",
  "status": "REJECTED"
}
"""

# 4. User Interface Front-End
st.subheader("Onboarding Evaluation Prompt:")
user_input = st.text_area(
    "Evaluation Scenario: 'What does a healthy boundary look like to you, and how do you handle it when a partner brings up a mistake you made?'",
    placeholder="Type response to analyze..."
)

if st.button("Execute Deep Behavioral Analysis"):
    if not api_key:
        st.error("Please enter the corresponding API key in the sidebar.")
    elif not user_input:
        st.warning("Please input text to execute analysis.")
    else:
        with st.spinner("Executing forensic linguistic processing via Codex generation model..."):
            try:
                # 5. Route Inference Based on Requirements
                if provider == "OpenAI GPT-5.6 (Official)":
                    import openai
                    client = openai.OpenAI(api_key=api_key.strip())
                    response = client.chat.completions.create(
                        model="gpt-5.6",
                        response_format={"type": "json_object"},
                        messages=[
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": user_input}
                        ]
                    )
                    raw_content = response.choices[0].message.content.strip()
                else:
                    from groq import Groq
                    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        response_format={"type": "json_object"},
                        messages=[
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": user_input}
                        ]
                    )
                    raw_content = response.choices[0].message.content.strip()

                # Parse JSON Output Safely
                parsed_result = json.loads(raw_content)
                st.success("Linguistic Analysis Complete!")
                
                # Visual Render Dashboard
                col1, col2, col3 = st.columns(3)
                col1.metric("Secure Alignment", f"{parsed_result.get('secure_rating', 0)}%")
                col2.metric("Covert Avoidance", f"{parsed_result.get('avoidant_rating', 0)}%")
                col3.metric("Toxic Risk Score", f"{parsed_result.get('toxic_risk_rating', 0)}%")
                
                st.write("### 🚨 Camouflage & Deception Index")
                st.progress(parsed_result.get('deception_score', 0) / 100)
                
                keywords = parsed_result.get('flagged_keywords', [])
                if keywords:
                    st.write("**Weaponized Terms Detected:** " + ", ".join([f"`{k}`" for k in keywords]))
                    
                st.info(f"**Gatekeeper Action:** {parsed_result.get('status', 'PENDING')}")
                st.write(f"**Psychological Rationale:** {parsed_result.get('justification')}")
                st.success(f"💡 **Secure Realignment:** \"{parsed_result.get('secure_translation')}\"")
                
            except Exception as e:
                st.error(f"Inference Connection Exception: {e}")
