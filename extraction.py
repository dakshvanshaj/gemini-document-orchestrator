
import pdfplumber 
from pathlib import Path
# we will also add logging for better debug information -> to do

# Extract text from PDF
def extract_text_from_pdf(pdf_path:Path) -> str:
    """
    Extracts text from a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.
    Returns:
        str: The extracted text from the PDF.
    """
    text = []

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            if page_text:
                text.append(f"--- Page {i + 1} ---\n{page_text}\n")
            else:
                print(f'Warning: No text found on page {i + 1}')
    

    return '\n'.join(text)

if __name__ == "__main__":

    pdf_path = Path('sample_input.pdf')
    if not pdf_path.exists():
        print(f'Error: The file {pdf_path} does not exist.')
    
    else:
        try:
            print(f'Attempting to extract text from {pdf_path}...')
            text = extract_text_from_pdf(pdf_path)
            print('Text extraction completed successfully.')

            print(f'Extracted {len(text)} characters of text.')

            print('--- Start of Extracted Text Preview ---')
            print(text)  
            print('--- End of Extracted Text Preview ---')
        except Exception as e:
            print(f'Error while extracting text: {e}')

    



