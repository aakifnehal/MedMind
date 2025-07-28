import streamlit as st
from utils.api import upload_pdfs_api


def render_uploader():
    st.sidebar.header("📄 Upload Medical Documents (.PDFs)")
    uploaded_files = st.sidebar.file_uploader(
        "Upload multiple PDFs", 
        type="pdf", 
        accept_multiple_files=True,
        help="Upload your medical documents for AI analysis"
    )
    
    if uploaded_files:
        st.sidebar.info(f"📁 {len(uploaded_files)} file(s) selected")
        for file in uploaded_files:
            st.sidebar.text(f"• {file.name}")
    
    if st.sidebar.button("🚀 Upload & Process", disabled=not uploaded_files) and uploaded_files:
        with st.sidebar:
            with st.spinner("Processing documents..."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("Uploading files...")
                progress_bar.progress(30)
                
                response = upload_pdfs_api(uploaded_files)
                progress_bar.progress(70)
                
                status_text.text("Processing content...")
                progress_bar.progress(100)
                
                if response.status_code == 200:
                    st.success("✅ Documents processed successfully!")
                    st.balloons()
                else:
                    st.error(f"❌ Error: {response.text}")