
import streamlit as st
from llm_api import generate_content
import re

# --- Session State for service status ---
if "service_status" not in st.session_state:
    st.session_state.service_status = "Available"
if "wait_time" not in st.session_state:
    st.session_state.wait_time = 0

# Demo content
DEMO_CONTENT = {
    "Blog Post": "Sample Blog Post: Embracing Remote Work can boost productivity...",
    "Tweet": "Demo Tweet: Remote work is changing the future of workplaces! 🚀",
    "LinkedIn Post": "Demo LinkedIn Post: Discover how remote work unlocks new opportunities.",
    "Product Description": "SmartBottle keeps drinks cold for 24 hrs. Perfect for daily use.",
    "Creative Story": "As the sun dipped below the horizon, a new adventure began...",
    "Marketing Email": "Boost your productivity with our new SmartPlanner. Limited offer!",
    "YouTube Script": "Welcome back to the channel! Today, we're diving into the future of AI...",
    "Code Snippet Explanation": "This Python snippet initializes a dictionary using a comprehension..."
}

st.set_page_config(page_title="AI Content Generator", page_icon="🧠")
st.title("🧠 AI Content Generator")
st.caption("Generate professional content with LLaMA-3 via Groq API")

st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Llama_glama_portrait.jpg/320px-Llama_glama_portrait.jpg", width=120)

st.info("""
**Note:** This app uses a free LLM API which may hit daily/hourly quota. If that happens, demo content will be shown.
""")

# --- Content type and tone customization ---
content_type = st.selectbox("Content Type", list(DEMO_CONTENT.keys()))
tone = st.selectbox("Tone", ["Default", "Formal", "Casual", "Humorous", "Empathetic"])
keywords = st.text_input("Optional keywords to include (comma-separated)")
topic = st.text_input("Topic or Prompt", help="e.g., 'Launch SmartBottle 2.0'")

max_tokens = st.slider("Output Length (tokens)", 50, 600, 150, 25)

if st.session_state.service_status == "Rate Limited":
    st.warning(f"⚠️ Rate-limited. Try again after {st.session_state.wait_time} seconds. Showing demo content below.")
else:
    st.success("✅ Service Status: Available")

if st.button("Generate Content"):
    if not topic:
        st.warning("Please enter a topic or prompt.")
    else:
        if st.session_state.service_status == "Rate Limited":
            st.info("Demo mode. Below is a sample output.")
            content = DEMO_CONTENT[content_type]
        else:
            with st.spinner("Generating content..."):
                try:
                    prompt = f"Write a {tone.lower()} {content_type.lower()} about: {topic}."
                    if keywords:
                        prompt += f" Include these keywords: {keywords}."
                    content = generate_content(prompt, max_tokens)
                    st.success("Content generated!")
                except Exception as e:
                    msg = str(e)
                    if any(k in msg.lower() for k in ["limit", "quota", "retry"]):
                        m = re.search(r"(\d+) seconds", msg)
                        wait_time = int(m.group(1)) if m else 60
                        st.session_state.service_status = "Rate Limited"
                        st.session_state.wait_time = wait_time
                        st.error(f"Quota reached. Switching to demo mode. Try again after {wait_time} seconds.")
                        content = DEMO_CONTENT[content_type]
                    else:
                        st.error(f"Error: {msg}")
                        content = ""

        if content:
            st.text_area("Generated Content", content, height=300)
            st.download_button("📥 Download as .txt", content, file_name="generated_content.txt")

st.caption("Powered by LLaMA-3 via Groq API. See quota usage: https://console.groq.com/usage")
st.markdown(
    """
    <hr style='margin-top:3rem; margin-bottom:1rem;'>
    <div style='text-align:center; font-size:0.9rem; color:#888;'>
        Built by <strong>Kaushal Dabhi</strong> • 
        <a href='https://github.com/kaushal-dabhi/Chatbot_Personality_Toggle' target='_blank' style='color:#1abc9c;'>GitHub Repo</a>
    </div>
    """,
    unsafe_allow_html=True
)




# --- Back link to main website ---
st.markdown(
    '''
    <div style='margin-top: 3rem; text-align: center;'>
        <a href="https://kaushaldabhi.com" target="_blank" style="font-size: 16px; color: #1abc9c;">
            ← Back to kaushaldabhi.com
        </a>
    </div>
    ''',
    unsafe_allow_html=True
)
