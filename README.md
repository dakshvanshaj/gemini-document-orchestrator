
## AI Powered Document Orchestrator

The system follows a linear flow where Streamlit acts as the control center, Python handles the initial "heavy lifting" (extraction), and n8n manages the business logic and external communication (email).

The Data Flow:


Input Layer (Streamlit): User uploads a PDF and asks a question.

Processing Layer 1 (Python Local):

Extract text from PDF (using pdfplumber or PyMuPDF).

Gemini Call 1: Send Text + User Question + JSON Schema to Gemini API.


Output: Receive structured JSON (e.g., {"risk_level": "High", "summary": "..."}) and display it to the user.


Trigger Layer (User Action): User reviews the JSON, enters an email address, and clicks "Send Alert Mail".

Processing Layer 2 (n8n Workflow):


Webhook: Receives JSON, Question, Text, and Email from Python.


Analysis: AI Agent generates a final analytical answer.


Logic: IF Node checks a condition (e.g., risk_level == 'High').


Action (True Branch): AI Agent drafts an email -> Email Node sends it.


Response: n8n returns the Answer, Email Body, and Status back to Streamlit.


Display Layer (Streamlit): UI updates to show the Final Answer, Email Body, and Status.