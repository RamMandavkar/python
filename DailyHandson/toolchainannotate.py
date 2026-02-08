# 1. Install required Libraries
#!pip install "langchain==1.2.7" langchain-google-genai google-generativeai
#!pip install langchain-classic
#!pip install langchain-openai
#!pip install --upgrade langchain langchain-core langchain-openai
#!pip install -U langchain langchain-openai

# 2. Define tools (add & multiply)
from langchain.tools import tool
from dotenv import load_dotenv
import os

load_dotenv()  # loads .env into environment

GEMINI_API_KEY = os.getenv("gemini_api_key")
GEMINI_MODEL_NAME = os.getenv("gemini_model_name")

@tool
def add(a: int, b: int) -> int:
    """Add two integers"""
    return a + b

@tool
def subtract(sum: int, b: int) -> int:
    """subtract two integers"""
    return sum - b

@tool
def multiply(subtract: int, b: int) -> int:
    """Multiply two integers"""
    return subtract * b

from google import genai

client = genai.Client(api_key=GEMINI_API_KEY)
# Register the tool and enable 'Automatic' calling
chat = client.chats.create(
    model=GEMINI_MODEL_NAME,
    config={
        'tools': [add, multiply, subtract]
    }
)

# Gemini will call the function, get the result, and summarize it in one go
response = chat.send_message("What is 12 plus 8? and then subtract 5 and then multiply the result by 2")
print(response.text)

response = chat.send_message("What is 12 plus 8? if the result greater then 19 then subtract 5 if the result less then 19 and then multiply the result by 2")
print(response.text)
