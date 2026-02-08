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
import requests
import os

load_dotenv()  # loads .env into environment

OPENWEATHER_API_KEY=  os.getenv("openweather_api_key")

@tool
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

# 3. Setup Gemini LLM (ChatGoogleGenerativeAI)
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# set your API key (or pass api_key=... when instantiating)
llm = ChatGoogleGenerativeAI(model=os.getenv("gemini_model_name"),
                             google_api_key=os.getenv("gemini_api_key"))

# 4. Create the agent (use create_agent instead of create_tool_calling_agent)
from langchain.agents import create_agent

agent = create_agent(
    model=llm,               # pass the model instance (or a model string)
    tools=[get_current_temperature],   # list of tool functions (decorated with @tool)
    system_prompt="You are a helpful OpenWeather assistant. Use tools when needed."
)

# 5. Run examples
resp1 = agent.invoke({"messages":[{"role":"user","content":"What's the temperature in Pune, Maharashtra? mentioned data as well"}]})
print(resp1["messages"][-1].content)
