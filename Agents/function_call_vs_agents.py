from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()  

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.0)

def get_weather(location: str) -> str:
    fake_data = {
        "Tokyo": "12°C, cloudy",
        "New York": "20°C, sunny",
        "London": "15°C, rainy"
    }
    return fake_data.get(location, "Location not found")

def calculate(expression: str) -> str:
    """2+3*2 -> 8"""
    try:
        result = eval(expression, {"__builtins__": {}})
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"
    
# Aprroach 1: Manual function calling loop    
def run_manual_function_calling(question: str) -> str:
    print(f"Question: {question}")

    tools_schema = [
        {
            "name": "get_weather",
            "description": "Get the current weather for a given location. Input should be a city name.",
            "parameters": {
                "type": "object",
                "properties":{
                    "city": {"type": "string"}
                },
            "required": ["city"]
            }
        },
        {
            "name": "calculate",
            "description": "Calculate a mathematical expression. Input should be a valid Python expression.",
            "parameters": {
                "type": "object",
                "properties":{
                    "expression": {"type": "string"}
                },
                "required": ["expression"]
            }
        }
    ]

    llm_with_tools = llm.bind_tools(tools_schema)

    messages = [HumanMessage(content=question)]
    response = llm_with_tools.invoke(messages)
    messages.append(response)

    if response.tool_calls:
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            print(f"  Detected tool call: {tool_name} with args {tool_args}")

            if tool_name == "get_weather":
                result = get_weather(tool_args["city"])
            elif tool_name == "calculate":
                result = calculate(tool_args["expression"])
            else:
                result = "Unknown tool"

            print(f"  Tool result: {result}")
            messages.append(ToolMessage(content=result, tool_call_id=tool_call["id"]))

        final_response = llm_with_tools.invoke(messages)
        return final_response.content
    else:
        return response.content

#Approach 2: Agentic solution using LangChain's AgentExecutor

@tool
def get_weather_tool(city: str) -> str:
    """Tool to get weather information for a city."""
    return get_weather(city)

@tool
def calculate_tool(expression: str) -> str:
    """Tool to calculate a mathematical expression."""
    return calculate(expression)

agent_tools = [get_weather_tool, calculate_tool]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an assistant that can answer questions using the following tools: get_weather and calculate."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

agent = create_tool_calling_agent(llm=llm, tools=agent_tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=agent_tools)

def run_agent(question: str) -> str:
    print(f"Question: {question}")
    response = agent_executor.invoke({"input": question})
    return response


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":
    questions = [
        "What is the weather like in Tokyo?",
        "What is (123 * 45) + 678?",
    ]

    print("=" * 60)
    print("APPROACH 1: LLM + Function Calling (manual loop)")
    print("=" * 60)
    for q in questions:
        answer = run_manual_function_calling(q)
        print(f"  Final answer: {answer}\n")

    print("=" * 60)
    print("APPROACH 2: Agentic Solution (LangChain AgentExecutor)")
    print("=" * 60)
    for q in questions:
        answer = run_agent(q)
        print(f"  Final answer: {answer}\n")