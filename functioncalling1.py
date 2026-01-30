# https://codeshare.io/5znW0j
# https://api.openweathermap.org/data/2.5/weather?q=pune&appid=b0b5a11ea058c69c6750f91d1a94b52f&units=metric
# https://home.openweathermap.org/api_keys
# https://ai.google.dev/gemini-api/docs/function-calling?_gl=1*9b43oy*_up*MQ..&gclid=Cj0KCQiAm9fLBhCQARIsAJoNOctCk6qv17GF3KK6RgP-O2gIbTJv8XWnD1xHBwcPyxmDxsGccW1VbqMaAvlCEALw_wcB&gbraid=0AAAAACn9t66I-TGG40cXLQo6NAptkHavl&example=meeting#python_2
# pip install google-genai
# pip install python-dotenv

## 1. Required Imports
from google import genai
from google.genai import types
import os
import requests


## 2. Setting API Keys
GEMINI_API_KEY = os.getenv("openai_api_key")
OPENWEATHER_API_KEY=  os.getenv("openweather_api_key") 

## 3. Function to be called
def get_current_temperature(location):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHER_API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        return data['main']['temp']
    else:
        raise Exception(f"Error fetching weather: {data.get('message', 'Unknown error')}")

## Testing if API KEY WORKS
## get_current_temperature("mumbai")
## On VSCode
if __name__ == "__main__":
    print(get_current_temperature("mumbai"))


