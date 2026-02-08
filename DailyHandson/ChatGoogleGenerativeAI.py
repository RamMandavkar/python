# pip install langchain
# pip install langchain_google_genai

from langchain_google_genai import ChatGoogleGenerativeAI  # pyright: ignore[reportMissingImports]
from dotenv import load_dotenv
import os

load_dotenv()  # loads .env into environment

llm = ChatGoogleGenerativeAI(model=os.getenv("gemini_model_name"),
                             google_api_key=os.getenv("gemini_api_key"))
response = llm.invoke("What is the capital of France?")
print(response)