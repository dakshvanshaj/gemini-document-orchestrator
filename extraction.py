
import pdfplumber 

# we will also add logging for better debug information -> to do

# Extract text from PDF
def extract_text_from_pdf(file_obj) -> str:
    """
    Extracts text from a PDF file.

    Args:
        file_obj: The file object of the PDF file.
    Returns:
        str: The extracted text from the PDF.
    """
    text = []

    # Use pdfplumber to open the PDF in bytes code
    with pdfplumber.open(file_obj) as pdf:
        for i, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            if page_text:
                text.append(f"--- Page {i + 1} ---\n{page_text}\n")
            else:
                print(f'Warning: No text found on page {i + 1}')
    

    return '\n'.join(text)

# Extract text from TXT
def extract_text_from_txt(file_obj):
    """
    Extracts text from a TXT file object.
    Args:
        file_obj: The file object of the TXT file.
    Returns:
        str: The extracted text from the TXT file."""
    # We read the bytes and decode them to a string (utf-8 is standard)
    try:
        return file_obj.read().decode("utf-8")
    except Exception as e:
        return f"Error reading text file: {e}"

# --- The Master Function ---
def process_file(uploaded_file):
    """
    Decides which function to use based on file type.
    Args:
        uploaded_file: The uploaded file object.
    Returns:
        str: The extracted text from the file."""
    
    # Streamlit file objects have a .name attribute we can check
    if uploaded_file.name.endswith('.pdf'):
        return extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith('.txt'):
        return extract_text_from_txt(uploaded_file)
    else:
        return "Unsupported file format."



# if __name__ == "__main__":

#     pdf_path = Path('sample_input.pdf')
#     if not pdf_path.exists():
#         print(f'Error: The file {pdf_path} does not exist.')
    
#     else:
#         try:
#             print(f'Attempting to extract text from {pdf_path}...')
#             text = extract_text_from_pdf(pdf_path)
#             text = extract_text_from_txt(txt_path)
#             print('Text extraction completed successfully.')

#             print(f'Extracted {len(text)} characters of text.')

#             print('--- Start of Extracted Text Preview ---')
#             print(text)  
#             print('--- End of Extracted Text Preview ---')
#         except Exception as e:
#             print(f'Error while extracting text: {e}')

    



