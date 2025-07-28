import streamlit as st
from utils.api import ask_question


def render_chat():
    st.subheader("💬 Chat with your MedMind")
    
    # Add helpful instructions
    if not st.session_state.get("messages"):
        st.info("👋 Welcome! Upload some medical documents first, then ask me questions about them.")
        st.markdown("""
        **Example questions:**
        - What are the key findings in my test results?
        - Summarize the treatment recommendations
        - What medications were prescribed?
        """)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Create a container for chat messages with max height
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                # Add timestamp
                if "timestamp" in msg:
                    st.caption(f"🕒 {msg['timestamp']}")

    # Input and response
    user_input = st.chat_input("Ask about your medical documents...")
    
    if user_input:
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M")
        
        # Add user message
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({
            "role": "user", 
            "content": user_input, 
            "timestamp": timestamp
        })

        # Show typing indicator
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                response = ask_question(user_input)
                
            if response.status_code == 200:
                data = response.json()
                answer = data["response"]
                sources = data.get("sources", [])
                
                st.markdown(answer)
                
                # Show sources in an expander
                if sources:
                    with st.expander("📚 View Sources"):
                        for i, src in enumerate(sources, 1):
                            st.markdown(f"**{i}.** `{src}`")
                
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": answer, 
                    "timestamp": timestamp,
                    "sources": sources
                })
            else:
                error_msg = f"❌ Sorry, I encountered an error: {response.text}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": error_msg, 
                    "timestamp": timestamp
                })

    # Add clear chat button
    if st.session_state.messages:
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🗑️ Clear Chat"):
                st.session_state.messages = []
                st.rerun()