import dotenv
import os
from google import genai
from google.genai import types 

# Load environment variables from .env file
dotenv.load_dotenv()

def ask_gemini(text: str, question: str, api_key: str):


    # Prompt for the Required Output format
    prompt = f"""
    I have a document with the following text:
    
    --- START OF DOCUMENT ---
    {text}
    --- END OF DOCUMENT ---
    
    Based ONLY on the text above, please answer this question:
    "{question}"
    """
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[prompt])

    return response.text

if __name__ == "__main__":

    text = """Brain rot is a term used to describe the feeling of mental fatigue or stagnation that can occur when someone is 
    exposed to too much of the same type of information or activity for an extended period. It can lead to a lack of motivation,
    creativity, and overall cognitive function. This can happen when people consume excessive amounts of low-quality content,
    such as mindless social media scrolling or repetitive tasks, which do not stimulate the brain in a meaningful way.
    To combat brain rot, it's important to take breaks, engage in diverse activities, and challenge the mind with new and 
    stimulating experiences."""

    question = 'Explain brain rot in simple terms but in detail'

    api_key = os.getenv('GEMINI_API_KEY')

    if not api_key:
        print('Error: GEMINI_API_KEY not found in environment variables.')

    else:
        print('Asking Gemini the question...')
        answer = ask_gemini(text, question, api_key)
        print('\n\n--- Answer ---')
        print(answer)