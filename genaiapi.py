# pip install google-genai
# pip install python-dotenv
from google import genai
import os

GEMINI_API_KEY = os.getenv("openai_api_key")

client = genai.Client(api_key=GEMINI_API_KEY)
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents='Tell me a story in 100 words.'
)
print(response.text)