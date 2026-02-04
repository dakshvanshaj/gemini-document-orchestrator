import streamlit as st
from extraction import extract_text_from_pdf

# --- LAYER 1: The Setup & "The Backpack" ---

st.set_page_config(page_title="Doc Orchestrator", layout="wide")

st.title("📄 AI Document Orchestrator")

# Check: Do we have a backpack yet?
if "doc_text" not in st.session_state:
    # If not, give the user an empty backpack to hold the text later
    st.session_state.doc_text = None 

# --- LAYER 2: Input & Extraction ---

with st.sidebar:
    st.header("1. Upload Document")
    
    # 1. The Widget: This creates the drag-and-drop box
    uploaded_file = st.file_uploader("Choose a PDF", type=["pdf"])
    
    # 2. The Trigger: As soon as a file is uploaded, this code runs
    if uploaded_file is not None:
        
        # We only want to extract if we haven't done it already 
        # (or if the user uploaded a NEW file)
        if st.session_state.doc_text is None:
            
            with st.spinner("Reading file..."):
                try:
                    # Pass the file object directly to your function
                    # pdfplumber.open() is smart enough to read this object!
                    extracted_text = extract_text_from_pdf(uploaded_file)
                    
                    # 3. The Save: Put the text in the backpack
                    st.session_state.doc_text = extracted_text
                    st.success("✅ Text Extracted Successfully!")
                    
                except Exception as e:
                    st.error(f"Error reading file: {e}")

# --- VISUAL CONFIRMATION ---
# This part is just for us to verify Layer 1 & 2 worked.
if st.session_state.doc_text:
    st.subheader("Raw Text Preview (stored in Session State):")
    st.text_area("Content", st.session_state.doc_text, height=300)
else:
    st.info("👈 Please upload a PDF in the sidebar to start.")