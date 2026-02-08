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
def subtract(a: int, b: int) -> int:
    """subtract two integers"""
    return a - b

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers"""
    return a * b
    

# 3. Setup Gemini LLM (ChatGoogleGenerativeAI)
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# set your API key (or pass api_key=... when instantiating)
llm = ChatGoogleGenerativeAI(model=GEMINI_MODEL_NAME,
                             google_api_key=GEMINI_API_KEY)

# 4. Create the agent (use create_agent instead of create_tool_calling_agent)
from langchain.agents import create_agent

agent = create_agent(
    model=llm,               # pass the model instance (or a model string)
    tools=[add, multiply, subtract],   # list of tool functions (decorated with @tool)
    system_prompt="You are a helpful math assistant. Use tools when needed."
)

# 5. Run examples
resp1 = agent.invoke({"messages":[{"role":"user","content":"What is 12 plus 8?"}]})
print(resp1["messages"][-1].content)

resp2 = agent.invoke({"messages":[{"role":"user","content":"Multiply 7 and 6"}]})
print(resp2["messages"][-1].content)

resp3 = agent.invoke({"messages":[{"role":"user","content":"subtract 7 and 6"}]})
print(resp3["messages"][-1].content)

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
response = chat.send_message("What is 12 plus 8?")
print(response.text)
