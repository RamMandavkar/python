# https://codeshare.io/5znW0j
# https://api.openweathermap.org/data/2.5/weather?q=pune&appid=b0b5a11ea058c69c6750f91d1a94b52f&units=metric
# https://home.openweathermap.org/api_keys
# https://ai.google.dev/gemini-api/docs/function-calling?_gl=1*9b43oy*_up*MQ..&gclid=Cj0KCQiAm9fLBhCQARIsAJoNOctCk6qv17GF3KK6RgP-O2gIbTJv8XWnD1xHBwcPyxmDxsGccW1VbqMaAvlCEALw_wcB&gbraid=0AAAAACn9t66I-TGG40cXLQo6NAptkHavl&example=meeting#python_2
# pip install google-genai
# pip install python-dotenv

## 1. Required Imports
from google import genai
from google.genai import types
from dotenv import load_dotenv
import requests
import os

load_dotenv()  # loads .env into environment
# -----------------------------
# 1. Set Your API Keys
# -----------------------------
# Replace with your own keys or use environment variables
## 2. Setting API Keys
GEMINI_API_KEY = os.getenv("gemini_api_key")
OPENWEATHER_API_KEY=  os.getenv("openweather_api_key") 

# -----------------------------
# 2. Define the Real Function
# -----------------------------
def get_current_temperature(location: str):
    """Fetch real-time temperature for a given location using OpenWeatherMap API."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    print ("tsee st :: ", data['main']['temp'])
    if response.status_code == 200:
        return data['main']['temp']
    else:
        raise Exception(f"Error fetching weather: {data.get('message', 'Unknown error')}")

if __name__ == "__main__":
  print(get_current_temperature("gurugram, haryana"))

# -----------------------------
# 3. Define Function Schema for Gemini
# Define Function Declaration: Define the function declaration in your application code. 
# Function Declarations describe the function's name, parameters, and purpose to the model.
# -----------------------------
weather_function = {
    "name": "get_current_temperature",
    "description": "Gets the current temperature for a given location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city name, e.g. San Francisco",
            },
        },
        "required": ["location"],
    },
}

# -----------------------------
# 4. Configure Gemini Client
# Call LLM with function declarations: Send user prompt along with the function declaration(s) to the model. 
# It analyzes the request and determines if a function call would be helpful. 
# If so, it responds with a structured JSON object.
# -----------------------------
client = genai.Client(api_key=GEMINI_API_KEY)
tools = types.Tool(function_declarations=[weather_function])
config = types.GenerateContentConfig(tools=[tools])

# -----------------------------
# 5. Send User Prompt to Gemini
# -----------------------------
user_prompt = "What's the temperature in gurugram, haryana? mentioned data as well"

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=user_prompt,
    config=config,
)

# -----------------------------
# 6. Check for Function Call and Execute
# -----------------------------
print("response  -> ",response)
first_part = response.candidates[0].content.parts[0]
print("first_part  -> ",first_part)
# Execute Function Code (Your Responsibility): The Model does not execute the function itself. 
# It's your application's responsibility to process the response and check for Function Call, 
if hasattr(first_part, "function_call") and first_part.function_call:
    function_call = first_part.function_call
    print(f"Function to call: {function_call.name}")
    print(f"Arguments: {function_call.args}")

    # Execute only if it's our weather function
    if function_call.name == "get_current_temperature":
        location = function_call.args.get("location")
        print("location: ",location)
        try:
            temperature = get_current_temperature(location)
            print(f"The current  temperature in {location} is {temperature}°C ")
        except Exception as e:
            print(f"Error: {e}")
else:
    # If Gemini doesn't call the function, just show its response
    print("No function call found. Gemini says:")
    print(response.text)
