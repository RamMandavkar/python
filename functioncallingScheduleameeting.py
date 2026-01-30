# https://codeshare.io/5znW0j
# https://api.openweathermap.org/data/2.5/weather?q=pune&appid=b0b5a11ea058c69c6750f91d1a94b52f&units=metric
# https://home.openweathermap.org/api_keys
# https://ai.google.dev/gemini-api/docs/function-calling?_gl=1*9b43oy*_up*MQ..&gclid=Cj0KCQiAm9fLBhCQARIsAJoNOctCk6qv17GF3KK6RgP-O2gIbTJv8XWnD1xHBwcPyxmDxsGccW1VbqMaAvlCEALw_wcB&gbraid=0AAAAACn9t66I-TGG40cXLQo6NAptkHavl&example=meeting#python_2
# pip install google-genai
# pip install python-dotenv

from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()  # loads .env into environment

GEMINI_API_KEY = os.getenv("openai_api_key")

# Define the function declaration for the model
schedule_meeting_function = {
    "name": "schedule_meeting",
    "description": "Schedules a meeting with specified attendees at a given time and date.",
    "parameters": {
        "type": "object",
        "properties": {
            "attendees": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of people attending the meeting.",
            },
            "date": {
                "type": "string",
                "description": "Date of the meeting (e.g., '2024-07-29')",
            },
            "time": {
                "type": "string",
                "description": "Time of the meeting (e.g., '15:00')",
            },
            "topic": {
                "type": "string",
                "description": "The subject or topic of the meeting.",
            },
        },
        "required": ["attendees", "date", "time", "topic"],
    },
}

# Configure the client and tools
client = genai.Client(api_key=GEMINI_API_KEY)
tools = types.Tool(function_declarations=[schedule_meeting_function])
config = types.GenerateContentConfig(tools=[tools])


# -----------------------------
# Send User Prompt to Gemini
# -----------------------------
#user_prompt = "What's the temperature in gurugram, haryana amd pune, maharashtra? mentioned data as well.   "
user_prompt = "Schedule a meeting with Bob and Alice for 03/14/2025 at 10:00 AM about the Q3 planning."

# Send request with function declarations
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=user_prompt,
    config=config,
)

print (response)
# Check for a function call
if response.candidates[0].content.parts[0].function_call:
    function_call = response.candidates[0].content.parts[0].function_call
    print(f"Function to call: {function_call.name}")
    print(f"Arguments: {function_call.args}")
    #  In a real app, you would call your function here:
    #  result = schedule_meeting(**function_call.args)
else:
    print("No function call found in the response.")
    print(response.text)