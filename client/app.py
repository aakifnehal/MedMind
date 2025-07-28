import streamlit as st
from components.upload import render_uploader
from components.history_download import render_history_download
from components.chatUI import render_chat


st.set_page_config(
    page_title="MedMind - AI Medical Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .stChatMessage {
        border-radius: 10px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🩺 MedMind</h1>
    <p>Your AI-Powered Medical Document Assistant</p>
</div>
""", unsafe_allow_html=True)

# Sidebar content
with st.sidebar:
    st.markdown("---")
    render_uploader()
    st.markdown("---")
    render_history_download()
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    MedMind helps you understand your medical documents using AI.
    
    **How to use:**
    1. Upload your PDF documents
    2. Ask questions about them
    3. Get AI-powered insights
    """)

# Main content
render_chat()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>MedMind v1.0 - AI Medical Assistant</div>",
    unsafe_allow_html=True
)