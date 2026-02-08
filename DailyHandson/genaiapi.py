# pip install google-genai
# pip install python-dotenv
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()  # loads .env into environment

GEMINI_API_KEY = os.getenv("gemini_api_key")

client = genai.Client(api_key=GEMINI_API_KEY)
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents='Tell me a story in 100 words.'
)
print(response.text)