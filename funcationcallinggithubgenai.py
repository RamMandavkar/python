# https://codeshare.io/5znW0j
# https://api.openweathermap.org/data/2.5/weather?q=pune&appid=b0b5a11ea058c69c6750f91d1a94b52f&units=metric
# https://home.openweathermap.org/api_keys
# https://ai.google.dev/gemini-api/docs/function-calling?_gl=1*9b43oy*_up*MQ..&gclid=Cj0KCQiAm9fLBhCQARIsAJoNOctCk6qv17GF3KK6RgP-O2gIbTJv8XWnD1xHBwcPyxmDxsGccW1VbqMaAvlCEALw_wcB&gbraid=0AAAAACn9t66I-TGG40cXLQo6NAptkHavl&example=meeting#python_2
# pip install google-genai
# pip install python-dotenv

## 1. Required Imports
from google import genai
from google.genai import types
import requests
import json
import os


# -----------------------------
# 1. Set Your API Keys
# -----------------------------
# Replace with your own keys or use environment variables

GEMINI_API_KEY = "AIzaSyCQpclA-oSpGvBqQ2LuDQODRyxqrq_-PyA"
GITHUB_TOKEN = "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"
USERNAME = "RamMandavkar"
REPOID = "182066833"
# -----------------------------
# 2. Define the Real Function
# -----------------------------
def get_github_details():
    #url = f"https://api.github.com/users/{USERNAME}/repos"
    url = f"https://api.github.com/repositories/{REPOID}"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(url, headers=headers)
    # print("response.json :: " , json.dumps(response.json(), indent=4))
    if response.status_code == 200:
    #    repos = response.json()
    #    for repo in repos:
    #       print(repo["full_name"])
    #       print("response.json :: ", json.dumps(repo.json(), indent=4) )
          return json.dumps(response.json(), indent=4)
    else:
       print("Error:", response.status_code, response.text)
    

# if __name__ == "__main__":
#    json_str = get_github_details() 
#    data = json.loads(json_str)
#    print(data.get("name"))

# ---------------------------------------------------------------------------------------
# 3. Define Function Schema for Gemini
# Define Function Declaration: Define the function declaration in your application code. 
# Function Declarations describe the function's name, parameters, and purpose to the model.
# ---------------------------------------------------------------------------------------
github_function = {
    "name": "get_github_details",
    "description": "Gets the current value for a given attribute.",
    "parameters": {
        "type": "object",
        "properties": {
            "value": {
                "type": "string",
                "description": "get value.",
            },
        },
        "required": ["value"],
    },
}

# -----------------------------
# 4. Configure Gemini Client
# Call LLM with function declarations: Send user prompt along with the function declaration(s) to the model. 
# It analyzes the request and determines if a function call would be helpful. 
# If so, it responds with a structured JSON object.
# -----------------------------
client = genai.Client(api_key=GEMINI_API_KEY)
tools = types.Tool(function_declarations=[github_function])
config = types.GenerateContentConfig(tools=[tools])

# -----------------------------
# 5. Send User Prompt to Gemini
# -----------------------------
user_prompt = "get deatils for value keys_url"

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=user_prompt,
    config=config,
)

# -----------------------------
# 6. Check for Function Call and Execute
# -----------------------------
#print("response  -> ",response)
first_part = response.candidates[0].content.parts[0]
#print("first_part  -> ",first_part)
# Execute Function Code (Your Responsibility): The Model does not execute the function itself. 
# It's your application's responsibility to process the response and check for Function Call, 
if hasattr(first_part, "function_call") and first_part.function_call:
    function_call = first_part.function_call
    print(f"Function to call: {function_call.name}")
    print(f"Arguments: {function_call.args}")

    # Execute only if it's our weather function
    if function_call.name == "get_github_details":
        key = function_call.args.get("value")
        print("key: ",key)
        try:
            json_str = get_github_details()
            data = json.loads(json_str)
            print(f"The current value for '{key}' is {data.get(key)}  ")
        except Exception as e:
            print(f"Error: {e}")
else:
    # If Gemini doesn't call the function, just show its response
    print("No function call found. Gemini says:")
    print(response.text)
