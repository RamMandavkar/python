import os
from google import genai
import os
import json
from google.genai.types import GenerateContentConfig
from dotenv import load_dotenv

load_dotenv()  # loads .env into environment

GEMINI_API_KEY = os.getenv("gemini_api_key")
GEMINI_MODEL_NAME = os.getenv("gemini_model_name")
# Configure the Gemini API
os.environ.setdefault("GEMINI_API_KEY", GEMINI_API_KEY)
print("API Key loaded successfully!")

# -------------------------------------------------------
# 2. Create GenAI Client
# -------------------------------------------------------
client = genai.Client()

# -------------------------------------------------------
# 3. Upload PDF File
# -------------------------------------------------------
def upload_pdf(file_path: str):
    uploaded_file = client.files.upload(file=file_path)
    print("Uploaded File Name:", uploaded_file.name)
    return uploaded_file


# -------------------------------------------------------
# 4. Extract Tags using LLM Prompt
# -------------------------------------------------------
def extract_pdf_tags(uploaded_file):
    
    prompt = """
    You are a document AI system.

    Task:
    Extract ALL tags/field names and their corresponding values from the provided PDF document.

    Instructions:
    - Identify labels like: Name, Account Number, IFSC, Date, Invoice No, Address, etc.
    - Return result strictly in JSON format.
    - JSON format should be:
      {
         "tag_name_1": "value",
         "tag_name_2": "value"
      }
    - Do not add explanations.
    - If no tags found, return empty JSON {}
    """

    response = client.models.generate_content(
        model=GEMINI_MODEL_NAME,#"gemini-1.5-pro",
        contents=[uploaded_file, prompt],
        config=GenerateContentConfig(
            temperature=0.2,
            response_mime_type="application/json"
        )
    )

    return response.text


# -------------------------------------------------------
# 5. Main Execution
# -------------------------------------------------------
def main():
    current_dir = os.getcwd()
    print("Current Directory:", current_dir)
    pdf_path = os.path.join(current_dir, "python/DailyHandson/docs/pdfreader.pdf")     

    uploaded_file = upload_pdf(pdf_path)

    llm_output = extract_pdf_tags(uploaded_file)

    print("\nRaw LLM Output:")
    print(llm_output)

    # ---------------------------------------------------
    # 6. Convert LLM output to Python dict safely
    # ---------------------------------------------------
    try:
        parsed_json = json.loads(llm_output)
        print("\nParsed JSON Output:")
        print(json.dumps(parsed_json, indent=4))
    except Exception as e:
        print("\nJSON Parsing Error:", str(e))


if __name__ == "__main__":
    main()
