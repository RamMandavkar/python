# 1. Install required Libraries
#!pip install "langchain==1.2.7" langchain-google-genai google-generativeai
#!pip install langchain-classic
#!pip install langchain-openai
#!pip install --upgrade langchain langchain-core langchain-openai
#!pip install -U langchain langchain-openai

# 2. Define tools (add & multiply)
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from dotenv import load_dotenv
import os

load_dotenv()  # loads .env into environment

GEMINI_API_KEY = os.getenv("gemini_api_key")
GEMINI_MODEL_NAME = os.getenv("gemini_model_name")

@tool
def get_user(user_id: str) -> dict:
    """Fetch user details"""
    return {
        "user_id": user_id,
        "name": "Ram",
        "balance": 1200,
        "status": "ACTIVE"
    }


@tool
def check_eligibility(user: dict) -> dict:
    """
    Check if user is eligible for payment.
    Rules:
    - Status must be ACTIVE
    - Balance must be >= 500
    """
    eligible = (
        user["status"] == "ACTIVE"
        and user["balance"] >= 500
    )

    return {
        "eligible": eligible,
        "reason": None if eligible else "User not eligible",
        "user": user
    }


@tool
def charge_payment(data: dict) -> dict:
    """
    Charge payment only if eligible.
    Deducts 500 from balance.
    """
    if not data["eligible"]:
        return {
            "charged": False,
            "message": "Payment skipped",
            "user": data["user"]
        }

    user = data["user"]
    user["balance"] -= 500

    return {
        "charged": True,
        "amount": 500,
        "user": user
    }


@tool
def notify_user(data: dict) -> str:
    """Notify user about payment result"""
    user = data["user"]

    if data.get("charged"):
        return f"Payment successful for {user['name']}. New balance: {user['balance']}"
    else:
        return f"Payment not processed for {user['name']}"


llm = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL_NAME,
    google_api_key=GEMINI_API_KEY
)

tools = [
    get_user,
    check_eligibility,
    charge_payment,
    notify_user
]

llm_with_tools = llm.bind_tools(tools)

prompt = """
Get user 101.
Check eligibility.
If eligible, charge payment.
Always notify the user.
"""

response = llm_with_tools.invoke(prompt)
print(response)
print(response.content)

