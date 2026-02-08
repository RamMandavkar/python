# https://github.com/dashboard
# ram.mandavkar@gmail.com/Ckmvrushali@1
# https://github.com/settings/personal-access-tokens/11019343
# pip install google-genai
# pip install python-dotenv
# pip install requests

from google import genai
from google.genai import types
from dotenv import load_dotenv
import requests
import os
import json

load_dotenv()  # loads .env into environment

GEMINI_API_KEY = os.getenv("gemini_api_key")
GITHUB_TOKEN = os.getenv("github_token")
USERNAME = os.getenv("github_username")

url = f"https://api.github.com/users/{USERNAME}/repos"

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

response = requests.get(url, headers=headers)
# print("response.json :: " , json.dumps(response.json(), indent=4))

if response.status_code == 200:
    repos = response.json()
    for repo in repos:
        print(repo["full_name"])
else:
    print("Error:", response.status_code, response.text)

# Define the function declaration for the model
fetchgithub_details_function = {
    "name": "fetchgithub_details",
    "description": "fetch github details with specified attributes.",
    "parameters": {
        "type": "object",
        "properties": {
            "attributes": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of attributes fetching from github.",
            },
        },
        "required": ["attributes"],
    },
}

# Configure the client and tools
client = genai.Client(api_key=GEMINI_API_KEY)
tools = types.Tool(function_declarations=[fetchgithub_details_function])
config = types.GenerateContentConfig(tools=[tools])

# -----------------------------
# Send User Prompt to Gemini
# -----------------------------
user_prompt = "query github for all attributes"

# Send request with function declarations
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=user_prompt,
    config=config,
)

print("Function to call response:",response.candidates[0].content.parts[0].function_call)

if response.candidates[0].content.parts[0].function_call:
    function_call = response.candidates[0].content.parts[0].function_call
    print(f"Function to call: {function_call.name}")
    print(f"Arguments: {function_call.args}")
    print("Arguments: ",function_call.args)
    for arg in function_call.args.get("attributes"):              
        print(arg)
        