# https://codeshare.io/ammvq4

import os
from google import genai
from dotenv import load_dotenv

load_dotenv()  # lo
# --- API KEY CONFIGURATION ---
# export GOOGLE_API_KEY="YOUR_API_KEY"
GEMINI_API_KEY = os.getenv("openai_api_key")

if not GEMINI_API_KEY:
    raise ValueError("Please set the GOOGLE_API_KEY environment variable.")

# --- CLIENT INITIALIZATION ---
client = genai.Client(api_key=GEMINI_API_KEY)


# --- SCAM DETECTION SYSTEM PROMPT ---
SCAM_DETECTION_SYSTEM_PROMPT = """
Role: You are a Simple Scam Detection System.

You analyze messages to determine whether they are scams.

Look for:
✓ Requests for money or personal information
✓ Urgent threats or pressure tactics
✓ Too-good-to-be-true offers
✓ Impersonation of legitimate services

Classification:
- Scam
- Not Scam
- Uncertain

Respond ONLY in valid JSON:

{
  "label": "Scam / Not Scam / Uncertain",
  "reasoning": "Why you classified it this way",
  "intent": "What the sender wants",
  "risk_factors": ["list of concerns"]
}
"""


def detect_scam(message: str) -> str:
    """Send message to Gemini and classify scam status"""

    combined_prompt = f"""
            {SCAM_DETECTION_SYSTEM_PROMPT}

            Message to analyze:
            \"\"\"{message}\"\"\"
            """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            {
                "role": "user",
                "parts": [{"text": combined_prompt}]
            }
        ],
    )

    return response.text


def chat_with_scam_detector():
    print("🔍 Scam Detection System (Gemini)")
    print("Paste a message to check if it's a scam.")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("Message: ")

        if user_input.lower() == "exit":
            print("Goodbye! Stay safe online 👋")
            break

        try:
            result = detect_scam(user_input)
            print("\nResult:")
            print(result)
            print("-" * 50)
        except Exception as e:
            print(f"Error: {e}")
            print("Please try again.\n")


if __name__ == "__main__":
    chat_with_scam_detector()
