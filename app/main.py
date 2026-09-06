import os
import sys

# Tell Python to look at the project root folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from app.agent import TrendPilotAgent
from app.memory import AgentMemory

st.set_page_config(page_title="TrendPilot - AI Content Agent", page_icon="🚀", layout="wide")

st.title("🚀 TrendPilot: Local Agentic Content Strategist")
st.caption("Powered by Local Ollama (Gemma 3:4B / Llama 3.2 3B) | AIRI Team PITB Task 2")

with st.sidebar:
    st.header("⚙️ Agent Settings")
    model_name = st.selectbox(
        "Local Model",
        ["llama3.2:3b", "gemma3:4b", "gemma2:2b", "phi3:mini", "qwen2.5:3b"],
        index=0
    )
    st.markdown("---")
    st.subheader("🧠 Memory (Past Runs)")
    memory = AgentMemory()
    history = memory.get_history()
    if history:
        for item in reversed(history[-5:]):
            st.markdown(f"**{item['topic']}** ({item['platform']})\n_{item['summary']}_")
    else:
        st.info("No prior history in memory.")

# Inputs
col1, col2 = st.columns([2, 1])
with col1:
    topic = st.text_input("Enter your Project or Topic:", value="YOLOv8 helmet safety detection project")
with col2:
    platform = st.selectbox("Target Platform:", ["LinkedIn", "Instagram Reels", "X / Twitter", "TikTok", "YouTube Shorts"])
    tone = st.selectbox("Tone:", ["Professional + Exciting", "Technical & Educational", "Humorous / Meme Style", "Storytelling / Vulnerable"])

if st.button("Generate Complete Viral Plan", type="primary"):
    with st.status("Agent Orchestration in Progress...", expanded=True) as status:
        agent = TrendPilotAgent(model=model_name)
        st.write("📋 Developing Strategy Plan...")
        output = agent.run(topic=topic, platform=platform, tone=tone)
        status.update(label="Agent completed all tasks successfully!", state="complete", expanded=False)

    # Render Results
    st.success(f"Output saved locally to: `{output['saved_file']}`")

    t1, t2, t3, t4, t5 = st.tabs(["📝 Caption & Hook", "🎬 Video Script", "🏷️ Hashtags", "🔍 Review & Plan", "📂 Raw Markdown"])

    with t1:
        st.subheader("Viral Hook")
        st.info(output["hook"])
        st.subheader("Post Body")
        st.markdown(output["caption"])

    with t2:
        st.subheader("Short-Form Video Script (30-45s)")
        st.code(output["script"], language="markdown")

    with t3:
        st.subheader("Selected Hashtags")
        st.write(" ".join(output["hashtags"]))

    with t4:
        st.subheader("Execution Plan")
        st.text(output["plan"])
        st.subheader("Reviewer QA Feedback")
        st.warning(output["review"])

    with t5:
        if os.path.exists(output["saved_file"]):
            with open(output["saved_file"], "r", encoding="utf-8") as f:
                st.code(f.read(), language="markdown")