import streamlit as st
import openai
import json

# 1. Setup Page Configurations
st.set_page_config(page_title="BabydollAI Gateway", page_icon="🛡️", layout="centered")
st.title("🛡️ SafeMatch AI: Onboarding Gateway")
st.write("Psychological preventative screening interface for high-value dating applications.")

# 2. Secure API Key Connection via Streamlit Secrets
openai.api_key = st.text_input("Enter OpenAI API Key to Test:", type="password")

# 3. Define the System Prompt Engine
SYSTEM_PROMPT = """
You are a world-class forensic psychologist specializing in adult attachment theory and relationship dynamics. 
Analyze the user's text onboarding response to calculate structural risk factors. 
Look past superficial charm to extract linguistic indicators of emotional unavailability, avoidant attachment, or toxic traits.
You MUST return a raw JSON object ONLY matching this schema precisely:
{
  "secure_rating": 0-100,
  "avoidant_rating": 0-100,
  "toxic_risk_rating": 0-100,
  "justification": "2-sentence psychological rationale.",
  "status": "APPROVED, FLAG_FOR_REVIEW, or REJECTED"
}
"""

# 4. Building the User Interface Front-End
st.subheader("Onboarding Evaluation Question:")
user_input = st.text_area(
    "Prompt: 'Describe a time a past partner didn't meet your expectations, and how you managed it.'",
    placeholder="Type your response here..."
)

if st.button("Submit Profile for Verification"):
    if not openai.api_key:
        st.error("Please enter an OpenAI API key to process.")
    elif not user_input:
        st.warning("Please input a sample text response to test.")
    else:
        with st.spinner("Analyzing linguistic psychological markers..."):
            try:
                # 5. Call OpenAI API Model
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    response_format={ "type": "json_object" },
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_input}
                    ]
                )

                # 6. Parse and Render Output
                result_json = json.loads(response.choices[0].message.content)

                st.success("Analysis Complete!")
                st.subheader("Platform Gateway Results")

                # Visual Metric Displays
                col1, col2, col3 = st.columns(3)
                col1.metric("Secure Score", f"{result_json['secure_rating']}%")
                col2.metric("Avoidant Score", f"{result_json['avoidant_rating']}%")
                col3.metric("Toxic Risk Score", f"{result_json['toxic_risk_rating']}%")

                st.info(f"**Gatekeeper Status:** {result_json['status']}")
                st.write(f"**Psychological Rationale:** {result_json['justification']}")

            except Exception as e:
                st.error(f"An error occurred: {e}")
