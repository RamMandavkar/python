## 0. The Imports
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()  # loads .env into environment

## 1. Setup the API Key
# Replace with your own keys or use environment variables
GEMINI_API_KEY = os.getenv("gemini_api_key")

client = genai.Client(api_key=GEMINI_API_KEY)

## 2. Defined a real function: add
def add(a:int, b:int) -> int:
  print(f"Executing add {a}, {b}")
  return a + b

available_functions = { "add": add }

## 3. Defined the Tool Schamas
add_decl = types.FunctionDeclaration(
    name="add",
    description="Adds two integers.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "a": types.Schema(type=types.Type.INTEGER, description="First integer"),
            "b": types.Schema(type=types.Type.INTEGER, description="Second integer"),
        },
        required=["a", "b"],
    ),
)

## 4. Created the Config
tools = [types.Tool(function_declarations=[add_decl])]
config = types.GenerateContentConfig(tools=tools)

## 5. Took the User Prompt
prompt="What is 3 + 4"
messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

## 6. First Tool Call
response_1 = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=messages,
    config=config
)



## 7. Inspect the outputs
content_1 = response_1.candidates[0].content
messages.append(content_1)


# 8. Execute any function_calls
tool_outputs = []
for part in content_1.parts:
    if part.function_call:
        name = part.function_call.name
        args = part.function_call.args
        print(f"> Function call: {name} with args {args}")
        fn = available_functions.get(name)
        try:
            result = fn(**args)
            tool_outputs.append(
                types.Part.from_function_response(name=name, response={"result": result})
            )
        except Exception as e:
            tool_outputs.append(
                types.Part.from_function_response(name=name, response={"error": str(e)})
            )


## 9. If any tools get called, use the second turn:
if tool_outputs:
  messages.append(types.Content(role="tool", parts=tool_outputs))
  response_2 = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=config
    )
  final = response_2.candidates[0].content
  print("".join([part.text for part in final.parts]))


content_1 = response_1.candidates[0].content
messages.append(content_1)