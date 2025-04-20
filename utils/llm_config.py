import os
from dotenv import load_dotenv
import google.generativeai as genai
import sys

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def get_llm_model():
    """Get the configured Gemini model"""
    return genai.GenerativeModel('gemini-2.0-flash')

def generate_response(model, prompt: str) -> str:
    """Generate response from LLM"""
    response = model.generate_content(prompt)
    return response.text

print(sys.path) 
