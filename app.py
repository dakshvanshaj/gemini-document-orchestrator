import streamlit as st
import requests
import os
from extraction import process_file
from brain import ask_gemini

from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

# --- LAYER 1: The Setup & "The Backpack" ---
api_key = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="Doc Orchestrator", layout="wide")
st.logo("logo.png", icon_image="icon.png")
st.title("📄 AI Document Orchestrator")

# Check: Do we have a stored document text yet?
if "doc_text" not in st.session_state:
    # If not, give the user an empty backpack to hold the text later
    st.session_state.doc_text = None 
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "user_query" not in st.session_state:
    st.session_state.user_query = None
# --- LAYER 2: Input & Extraction ---

with st.sidebar:
    st.header("1. Upload Document")
    
    # 1. The Widget: This creates the drag-and-drop box
    uploaded_file = st.file_uploader("Choose a PDF", type=["pdf", "txt"])
    
    # 2. The Trigger: As soon as a file is uploaded, this code runs
    if uploaded_file is not None:
        
        # We only want to extract if we haven't done it already 
        # (or if the user uploaded a NEW file)
        if st.session_state.doc_text is None:
            
            with st.spinner("Reading file..."):
                try:
                    # Pass the file object directly to your function
                    # pdfplumber.open() is smart enough to read this object!
                    extracted_text = process_file(uploaded_file)
                    
                    # 3. The Save: Put the text in the backpack
                    st.session_state.doc_text = extracted_text
                    st.success("✅ Text Extracted Successfully!")
                    
                except Exception as e:
                    st.error(f"Error reading file: {e}")

    st.divider()
    st.header("2. Query Document")

    # question box
    user_query = st.text_area("What do you want to know?", 
                        value="What are the key risks and dates?",
                        height=100)

# --- LAYER 3: The Brain (Trigger) ---
# This is where we will call the brain script that sends the text and question to Gemini.

    # Only show the button if we have text to work with
    if st.session_state.doc_text:
        if st.button("🤖 Analyze Document", type='primary'):

            if not api_key:
                st.error("⚠️ GEMINI_API_KEY not found in .env")
            else:

                # save the user query in state as well for N8N
                st.session_state.user_query = user_query

                with st.spinner("Analyzing document with Gemini..."):
                    
                    try:

                        result = ask_gemini(
                            st.session_state.doc_text, 
                            user_query, 
                            api_key
                        )

                        # Save the result in session state
                        st.session_state.analysis_result = result
                    except Exception as e:
                        st.error(f"Analysis Failed: {e}")

# --- LAYER 4: The Display (Main Page) ---
# We only show results if they exist in the backpack

if st.session_state.analysis_result:
    
    result = st.session_state.analysis_result

    # 1. High-Level Summary Block
    st.subheader("Analysis Results")

# Create 3 columns for quick metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"**Summary:** {result.summary}")
        
    with col2:
        # Dynamic color based on risk level
        risk = result.risk_level
        if risk == "High":
            st.error(f"🚨 **Risk Level:** {risk}")
        elif risk == "Medium":
            st.warning(f"⚠️ **Risk Level:** {risk}")
        else:
            st.success(f"✅ **Risk Level:** {risk}")

    st.divider()

    # 2. The Structured Data (The "Key-Value Pairs")
    st.subheader("Detailed Extraction")
    
    # We display this as a nice table
    # We convert the list of Pydantic objects to a list of dicts for Streamlit
    data_for_table = [
        {"Attribute": item.key, "Value": item.value} 
        for item in result.relevant_attributes
    ]
    st.table(data_for_table)
    
    # 3. Raw JSON (Useful for debugging and "Transparency")
    with st.expander("View Raw JSON (for Developer)"):
        # We dump the raw Pydantic model to JSON
        st.json(result.model_dump())

    st.divider()
    st.subheader("Automated Email Alert")

    # A container makes the email section look distinct
    with st.container(border=True):
        col_email, col_btn = st.columns([3, 1])
        
        with col_email:
            recipient_email = st.text_input("Recipient Email", placeholder="manager@company.com")
            
        with col_btn:
            # Add spacing so the button aligns with the input box
            st.write("") 
            st.write("")
            send_btn = st.button("🚀 Send Alert Mail", type="primary", use_container_width=True)

        if send_btn:
            # 1. Validation
            if not recipient_email:
                st.warning("⚠️ Please enter an email address.")
            else:
                with st.spinner("Triggering n8n Workflow..."):
                    try:
                        
                        # 2. Pack the Digital Envelope (The Payload)
                        payload = {
                            "recipient_email": recipient_email,
                            # Use the snapshot we saved earlier
                            "user_query": st.session_state.get('user_query'),
                            "extracted_data": result.model_dump(),
                            "text_context": st.session_state.doc_text[:5000] # Limit text size
                        }

                        # 3. Send to n8n
                        webhook_url = os.getenv("N8N_WEBHOOK_URL")
                        if not webhook_url:
                            st.error("Missing N8N_WEBHOOK_URL in .env")
                        else:
                            # POST request to your n8n local server
                            response = requests.post(webhook_url, json=payload)
                            
                            # 4. Handle Response
                            if response.status_code == 200:
                                # Parse the JSON first
                                n8n_data = response.json()
                                
                                st.success("✅ Workflow Triggered Successfully!")
                                
                                # Show Raw Data 
                                with st.expander("Debug Raw Response"):
                                    st.json(n8n_data)
                                
                                # Show formatted results
                                st.subheader("🤖 Final Analysis from n8n")
                                st.info(n8n_data.get('final_answer', 'No answer returned'))
                                
                                st.subheader("📧 Email Status")
                                if n8n_data.get('email_body'):
                                    st.html(n8n_data.get('email_body'))
                                else:
                                    st.warning("Email was not sent (Risk condition likely not met).")
                                    
                            else:
                                st.error(f"❌ Failed: {response.status_code}")
                                st.text(response.text)

                    except Exception as e:
                        st.error(f"Connection Error: {e}")

else:
    # Empty state message
    if not st.session_state.doc_text:
        st.info("👈 Waiting for file upload...")
    else:
        st.info("👈 File loaded. Click 'Analyze Document' to proceed.")

