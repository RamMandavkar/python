# 1. Install required Libraries
#!pip install "langchain==1.2.7" langchain-google-genai google-generativeai
#!pip install langchain-classic
#!pip install langchain-openai
#!pip install --upgrade langchain langchain-core langchain-openai
#!pip install -U langchain langchain-openai

# 2. Define tools (add & multiply)
from langchain_core.tools import tool
from dotenv import load_dotenv
import os
import json

load_dotenv()  # loads .env into environment

GEMINI_API_KEY = os.getenv("gemini_api_key")
GEMINI_MODEL_NAME = os.getenv("gemini_model_name")

# ==============================
# 2. Load Text File
# ==============================
# Get current working directory
current_dir = os.getcwd()
print("Current Directory:", current_dir)

@tool
def getBorrowerDetails(record_id: str) -> dict:    
    """
    Reads a JSON file containing a single object and returns it as a dictionary.

    Args:
        record_id (str): ID of the borrower record to retrieve

    Returns:
        dict: JSON object
    """
    file_path = os.path.join(current_dir, "python/DailyHandson/docs/BorrowerDetails.json")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Ensure JSON contains single object
    if not isinstance(data, dict):
        raise ValueError("JSON must contain a single object")

    return data
    
@tool
def getCOlltralProviderDetails(record_id: str) -> dict:    
    """
    Reads a JSON file containing a single object and returns it as a dictionary.

    Args:
        record_id (str): ID of the collateral provider record to retrieve

    Returns:
        dict: JSON object
    """
    file_path = os.path.join(current_dir, "python/DailyHandson/docs/CPDetails.json")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Ensure JSON contains single object
    if not isinstance(data, dict):
        raise ValueError("JSON must contain a single object")

    return data

# Example direct call
#if __name__ == "__main__":
#    result = getBorrowerDetails.invoke("MB123456")
#    print(result)
#    result = getCOlltralProviderDetails.invoke("CP123456")
#    print(result)
    

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
    tools=[getBorrowerDetails, getCOlltralProviderDetails],   # list of tool functions (decorated with @tool)
    system_prompt="You are a helpful data validation assistant. Use tools when needed." \
    "Club the all outputs and return as final output in arrary format. DO not return any intermediate output." \
    "do not to halogenate"
)

# 5. Run examples
prompt = """
Get borrower details for borrower ID 101 but do not return any intermediate output.
Get collateral provider details for collateral provider ID CP123456 but do not return any intermediate output.
If borrower "kycStatus" is "Verified" and collateral provider "industry_context" is "risk management" then return "MLTCNEW"
If borrower "employmentType" is "Salaried" and collateral provider one of "company_name" is "Indian Commodities" includes "NBFCs" partners in it "key_banking_partners" then return "MLTCAMD"
"""
resp1 = agent.invoke({"messages":[{"role":"user","content":prompt}]})
print(resp1["messages"][-1].content)
