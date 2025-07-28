import streamlit as st
import datetime


def render_history_download():
    if st.session_state.get("messages"):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("### 📋 Chat Session")
            st.caption(f"💬 {len(st.session_state.messages)} messages")
        
        with col2:
            # Format chat history nicely
            chat_text = f"MedMind Chat History\nGenerated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            chat_text += "=" * 50 + "\n\n"
            
            for i, msg in enumerate(st.session_state.messages, 1):
                role = "👤 USER" if msg["role"] == "user" else "🤖 ASSISTANT"
                timestamp = msg.get("timestamp", "")
                chat_text += f"{i}. {role} ({timestamp}):\n{msg['content']}\n\n"
                
                # Add sources if available
                if msg.get("sources"):
                    chat_text += "📚 Sources:\n"
                    for src in msg["sources"]:
                        chat_text += f"  - {src}\n"
                    chat_text += "\n"
                
                chat_text += "-" * 30 + "\n\n"
            
            st.download_button(
                "📥 Download History",
                chat_text,
                file_name=f"medmind_chat_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                help="Download your complete chat history"
            )