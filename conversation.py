# https://codeshare.io/G6JKjO
# pip install openai
# pip install dotenv

from openai import OpenAI
from dotenv import load_dotenv
import os

# 2. Initialize conversation history
messages = [
    {"role": "system", 
     "content": "You are a movie buff, "
     "you only reply to what is asked for and in very concise manner with comma separated lists wherever applicable. "
     "Clean the responses without system instruction as the user only needs the response"},    
]

load_dotenv()  # loads .env into environment

def ask_question(question, messages):
    # Instantiate an OpenAI Client
    client = OpenAI(
        api_key=os.getenv("openai_api_key"),
        base_url=os.getenv("openai_base_url")
    )

    messages.append({"role": "user", "content": question})

    # 3. Send first request
    response = client.chat.completions.create(
        model=os.getenv("gemini_model_name"),  # Use Gemini model name
        messages=messages
    )
    assistant_reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": assistant_reply})
    print(assistant_reply)
    return assistant_reply
    
## On Colab
#ask_question("Who directed the movie Inception?", messages)
#ask_question("What other movies has he directed?", messages)


## On VSCode
if __name__ == "__main__":
  ask_question("Who directed the movie Inception?", messages)
  ask_question("What other movies has he directed?", messages)  
