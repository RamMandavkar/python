from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import subprocess
import json

load_dotenv()  # loads .env into environment

GEMINI_API_KEY = os.getenv("gemini_api_key")
GEMINI_MODEL_NAME = os.getenv("gemini_model_name")
# Configure the Gemini API
os.environ.setdefault("GEMINI_API_KEY", GEMINI_API_KEY)
print("API Key loaded successfully!")

# -------------------------------------------------------
# 2. Create GenAI Client
# -------------------------------------------------------
client = genai.Client(api_key=GEMINI_API_KEY)

# ---------------------------------------------------
# SEND PDF DIRECTLY TO GEMINI (NO EXTRA LIBS)
# ---------------------------------------------------

def extract_pdf_tags(pdf_path: str) -> dict:
    """
    Sends PDF directly to Gemini and extracts all tags/values.
    """

    # Read PDF as binary
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    prompt = """
    You are an intelligent PDF document parser.

    Extract ALL possible tags/fields and corresponding values.

    Rules:
    - Return STRICT JSON only.
    - Keys must be field names.
    - Values must be field values.
    - If repeated, return list.
    - No explanation.
    """

    response = client.models.generate_content(
        model=GEMINI_MODEL_NAME, # "gemini-2.0-flash"
        contents=[
            types.Part.from_bytes(
                data=pdf_bytes,
                mime_type="application/pdf",
            ),
            prompt,
        ],
    )

    try:
        return json.loads(response.text)
    except Exception:
        print("Model did not return strict JSON:")
        print(response.text)
        return {}


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

if __name__ == "__main__":
    current_dir = os.getcwd()
    print("Current Directory:", current_dir)
    pdf_file_path = os.path.join(current_dir, "python/DailyHandson/docs/pdfreader.pdf") 
    result = extract_pdf_tags(pdf_file_path)
    print(json.dumps(result, indent=4))