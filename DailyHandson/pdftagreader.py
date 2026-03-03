import os
from pydantic import BaseModel, Field
import pypdf
from pypdf import PdfReader
from google import genai
import os
from google.genai import types
from dotenv import load_dotenv

load_dotenv()  # loads .env into environment

GEMINI_API_KEY = os.getenv("gemini_api_key")
GEMINI_MODEL_NAME = os.getenv("gemini_model_name")
# Configure the Gemini API
os.environ.setdefault("GEMINI_API_KEY", GEMINI_API_KEY)
print("API Key loaded successfully!")

# ---------------------------------------------------------------------------
# 1. Define Pydantic Schemas for Structured Output
# ---------------------------------------------------------------------------
class DocumentTag(BaseModel):
    tag_name: str = Field(description="The name of the field, category, or tag identified in the document.")
    value: str = Field(description="The specific value corresponding to the tag.")

class ExtractedData(BaseModel):
    extracted_tags: list[DocumentTag] = Field(
        description="A comprehensive list of all key-value tags found in the document based on the prompt."
    )

# ---------------------------------------------------------------------------
# 2. PDF Text Extraction
# ---------------------------------------------------------------------------
def extract_text_from_pdf(pdf_path: str) -> str:
    """Reads a PDF and extracts all available text."""
    try:
        reader = pypdf.PdfReader(pdf_path)
        full_text = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                full_text.append(page_text)
        return "\n".join(full_text)
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

# ---------------------------------------------------------------------------
# 3. LLM Processing via google-genai
# ---------------------------------------------------------------------------
def extract_tags_with_gemini(pdf_text: str, instruction_prompt: str) -> ExtractedData | None:
    """Sends the extracted text and prompt to Gemini, returning a Pydantic object."""
    # The client automatically picks up the GEMINI_API_KEY environment variable
    client = genai.Client()
    
    # We use a reliable, fast model for standard text extraction tasks
    model_id = GEMINI_MODEL_NAME 

    combined_prompt = f"""
    {instruction_prompt}

    --- PDF TEXT START ---
    {pdf_text}
    --- PDF TEXT END ---
    """

    try:
        response = client.models.generate_content(
            model=model_id,
            contents=combined_prompt,
            config=types.GenerateContentConfig(
                # Enforce JSON output matching our Pydantic schema
                response_mime_type="application/json",
                response_schema=ExtractedData,
                temperature=0.1 # Low temperature for factual extraction
            )
        )
        
        # The new SDK automatically parses the JSON into the Pydantic model
        return response.parsed
    
    except Exception as e:
        print(f"Error communicating with Gemini: {e}")
        return None

# ---------------------------------------------------------------------------
# 4. Main Execution
# ---------------------------------------------------------------------------
if __name__ == "__main__":    
    # Ensure your API key is available
    if not os.environ.get("GEMINI_API_KEY"):
        print("Warning: GEMINI_API_KEY environment variable is not set.")
    
    current_dir = os.getcwd()
    print("Current Directory:", current_dir)
    sample_pdf_path = os.path.join(current_dir, "python/DailyHandson/docs/pdfreader.pdf") 
    
    # Customize this prompt based on what exactly you want to extract
    user_prompt = """
    Analyze the provided document text. 
    Extract every relevant data point as a tag-value pair.
    """

    if not os.path.exists(sample_pdf_path):
        print(f"Please place a valid PDF file named '{sample_pdf_path}' in the directory.")
    else:
        print("Extracting text from PDF...")
        text_content = extract_text_from_pdf(sample_pdf_path)
        
        if text_content.strip():
            print("Sending text to Gemini for extraction...")
            result = extract_tags_with_gemini(text_content, user_prompt)
            
            if result:
                print("\n--- Extracted Tags ---")
                for item in result.extracted_tags:
                    print(f"• {item.tag_name}: {item.value}")
            else:
                print("Failed to extract data.")
        else:
            print("No text could be extracted from the PDF. It might be an image-based/scanned PDF.")
