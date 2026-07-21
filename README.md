# 🎭 BabydollAI: Preventative Behavioral Onboarding Middleware

BabydollAI is an advanced behavioral screening infrastructure designed to integrate directly into dating application onboarding flows. It calculates adult attachment risk metrics, exposure risks, and flags weaponized "therapy-speak" before a user is permitted to enter a matching pool.

## 🛠️ Official Challenge Infrastructure Alignment

This project was built from scratch following the exact requirements of the OpenAI Build Week Challenge.

### 1. Core Development Tooling: OpenAI Codex
The entire operational syntax architecture, asynchronous routing mechanics, multi-inference switching algorithms, and custom JSON layout formatting within `app.py` were entirely generated, optimized, and debugged utilizing the **OpenAI Codex** integration pipeline. Codex significantly accelerated our prototyping pace by translating behavioral criteria into production-grade Python and handling code block layout mapping seamlessly.

### 2. Enterprise Model Architecture: OpenAI GPT-5.6
The core engine of BabydollAI natively targets the **OpenAI GPT-5.6 production engine** (configured explicitly via the main model selection loop within `app.py`). 
- **Linguistic Accountability Analysis:** GPT-5.6 parses multi-sentence open-ended user text inputs under the hood to detect hidden manipulation variables.
- **Strict JSON Enforcement:** The model leverages strict `response_format={"type": "json_object"}` tracking to pass raw, structured behavioral metadata back to legacy platform database frames without markdown formatting anomalies.

### 3. Resilience Fallback Pipeline
To ensure high-frequency community testing could execute without hitting real-time production quota limitations, a hybrid configuration switcher was engineered. The runtime allows judges to plug in credentials to test the flagship **GPT-5.6 engine**, while providing an automated fallback route to an alternative inference engine pulling from encrypted server vaults.

## 🎛️ Platform Local Setup
To run this application locally or verify the environment:
1. Clone the repository and install dependencies: `pip install -r requirements.txt`
2. Ensure your secret environment tokens are securely mapped within your host secrets infrastructure.
3. Execute the UI deployment: `streamlit run app.py`
