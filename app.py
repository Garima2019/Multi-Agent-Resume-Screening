from dotenv import load_dotenv
load_dotenv()  # MUST be before CrewAI imports

import streamlit as st
from crew_logic import build_crew
from callbacks import StreamlitCallback

st.set_page_config(page_title="Multi-Agent Evaluator", layout="wide")
st.title("🧠 Multi-Agent Evaluation System")

user_input = st.text_area("Enter your input for evaluation")

show_logs = st.sidebar.checkbox("Show live agent logs", value=False)

if "final_result" not in st.session_state:
    st.session_state.final_result = None

if st.button("Run Evaluation"):
    if not user_input.strip():
        st.warning("Enter some input first.")
    else:
        with st.spinner("Agents are working..."):
            log_container = st.empty() if show_logs else None
            callback = StreamlitCallback(log_container) if show_logs else None

            crew = build_crew(user_input, callback)
            result = crew.kickoff()

            st.session_state.final_result = result

if st.session_state.final_result:
    st.subheader("✅ Final Output")
    st.write(st.session_state.final_result)
