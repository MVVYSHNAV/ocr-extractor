import streamlit as st
import os
import tempfile
import json
import time
from datetime import datetime

from ocrapp.core.orchestrator import DocumentExtractor

st.set_page_config(
    page_title="Smart Document Extractor",
    page_icon="📄",
    layout="wide"
)

# Apply custom styling via raw HTML/CSS
st.markdown("""
<style>
    .reportview-container {
        flex-direction: column;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .winner-card {
        background-color: #f0fdf4;
        border-left: 5px solid #22c55e;
        padding: 20px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .winner-card h3 {
        color: #166534;
        margin-top: 0;
    }
    .debug-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 15px;
        border-radius: 5px;
        margin-top: 20px;
        color: #0f172a;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_extractor():
    return DocumentExtractor()

def save_result(filename, result):
    # Create results folder if it doesn't exist
    os.makedirs("results", exist_ok=True)
    
    # Save the text
    base_name = os.path.splitext(filename)[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = f"results/{base_name}_{timestamp}_extracted.txt"
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(result["text"])
        
    return out_path

def main():
    st.title("📄 Smart Document Extractor")
    st.markdown("""
    Upload a document (PDF, DOCX, Images, HTML) below. The engine will route the file to multiple extraction libraries (like Docling, EasyOCR, PyMuPDF, etc.), score their outputs, and automatically pick the highest fidelity result!
    """)
    
    # Initialize session state for retaining extraction results
    if 'processing_result' not in st.session_state:
        st.session_state.processing_result = None
    if 'last_uploaded_file' not in st.session_state:
        st.session_state.last_uploaded_file = None

    uploaded_file = st.file_uploader("Choose a file to extract...", type=['pdf', 'png', 'jpg', 'jpeg', 'docx', 'html', 'txt'])
    
    if uploaded_file is not None:
        # If user uploads a new file, reset the result
        if st.session_state.last_uploaded_file != uploaded_file.name:
            st.session_state.processing_result = None
            st.session_state.last_uploaded_file = uploaded_file.name
            
        process_button = st.button("Extract Text", type="primary", use_container_width=True)
        
        if process_button:
            with st.spinner("Initializing Extractors (Heavy models may take a moment)..."):
                extractor = get_extractor()
                
            with st.spinner(f"Extracting '{uploaded_file.name}' using multiple engines..."):
                # Save uploaded file to a temporary location for the extractors to read
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                    
                try:
                    start_time = time.time()
                    result = extractor.process(tmp_path)
                    process_time = time.time() - start_time
                    result['process_time'] = process_time
                    st.session_state.processing_result = result
                except Exception as e:
                    st.error(f"An error occurred during extraction: {str(e)}")
                finally:
                    # Clean up temp file
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)
                        
    # Display results if available
    if st.session_state.processing_result:
        res = st.session_state.processing_result
        
        st.markdown("---")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"""
            <div class="winner-card">
                <h3>🏆 Best Extractor: <b>{res['source']}</b></h3>
                <p style="margin-bottom: 0;"><b>Confidence Score:</b> {res['score']:.2f} / 100 
                | <b>Processing Time:</b> {res.get('process_time', 0):.2f}s</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            # Create download button
            st.download_button(
                label="⬇️ Download Raw Text",
                data=res['text'],
                file_name=f"{st.session_state.last_uploaded_file}_extracted.txt",
                mime="text/plain",
                use_container_width=True
            )
            
            # Save to disk functionality
            if st.button("📁 Save to Results Folder", use_container_width=True):
                out_path = save_result(st.session_state.last_uploaded_file, res)
                st.success(f"Saved locally to `{out_path}`")
                
        # Layout for Text Preview and Debug Stats
        tab1, tab2 = st.tabs(["📝 Text Preview", "📊 Engine Debug Metrics"])
        
        with tab1:
            st.text_area("Extraction Results", value=res['text'], height=500, disabled=False)
            
        with tab2:
            st.markdown("### Scoring Breakdown by Engine")
            st.markdown("The orchestrator evaluated these engines but rejected them in favor of the winner:")
            
            for debug_info in sorted(res.get("debug", []), key=lambda x: x["score"], reverse=True):
                if debug_info['source'] == res['source']:
                    continue # Skip winner
                    
                status_icon = "❌ Error" if debug_info.get("score", -1) < 0 else "⚠️ Rejected"
                score_display = f"{debug_info['score']:.2f}" if debug_info.get("score", -1) >= 0 else "Failed"
                err_msg = f"<br><i>Reason: {debug_info['error']}</i>" if "error" in debug_info else ""
                
                st.markdown(f"""
                <div class="debug-card">
                    <b>Engine:</b> {debug_info['source']} <span style="float:right;">{status_icon}</span><br>
                    <b>Score:</b> {score_display} {err_msg}
                </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
