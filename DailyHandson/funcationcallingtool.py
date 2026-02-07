#https://codeshare.io/GkDBLp refer ink 

from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()  # loads .env into environment
# Replace with your own keys or use environment variables
GEMINI_API_KEY = os.getenv("openai_api_key")

client = genai.Client(api_key=GEMINI_API_KEY)

def add(a:int, b:int) -> int:
  print(f"Executing add {a}, {b}")
  return a + b

available_functions = { "add": add }

add_decl = types.FunctionDeclaration(
    name="add",
    description="Adds two integers.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "a": types.Schema(type=types.Type.INTEGER, description="First integer"),
            "b": types.Schema(type=types.Type.INTEGER, description="Second integer"),
        },
        required=["a", "b"],
    ),
)

if __name__ == "__main__":
  print(add(1,1))

