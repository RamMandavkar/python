# Step 1: Install Packages
# pip install langchain langchain-community langchain-google-genai google-genai faiss-cpu python-dotenv
# ==============================
# 1. Imports
# ==============================
import os
from google import genai
import sys
# LangChain imports
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os
# Sentence Transformer
from sentence_transformers import SentenceTransformer
from langchain.embeddings.base import Embeddings

load_dotenv()  # loads .env into environment
## 1. Setup the API Key
# Replace with your own keys or use environment variables
GEMINI_API_KEY = os.getenv("gemini_api_key")
print("GEMINI_API_KEY:", GEMINI_API_KEY)
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY
GEMINI_MODEL_NAME=os.getenv("gemini_model_name")
# -----------------------------
# 1️⃣ Custom Embedding Wrapper
# -----------------------------
class SentenceTransformerEmbeddings(Embeddings):
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts):
        return self.model.encode(texts).tolist()

    def embed_query(self, text):
        return self.model.encode(text).tolist()
    
# ==============================
# 2. Load Text File
# ==============================
# Get current working directory
current_dir = os.getcwd()
print("Current Directory:", current_dir)

# Create full file path
file_path = os.path.join(current_dir, "\\docs\\companypolicy.txt")

print("File Path:", file_path)
loader = TextLoader("python/DailyHandson/docs/companypolicy.txt") # your text file
documents = loader.load()
print("Loaded Documents:", len(documents))
sys.exit(0)

# ==============================
# 3. Split Text into Chunks
# ==============================
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20
)

split_docs = text_splitter.split_documents(documents)

print("Total Chunks:", len(split_docs))

# -----------------------------
# 4️⃣ Create Embeddings
# -----------------------------
embedding_model = SentenceTransformerEmbeddings()

# -----------------------------
# 5️⃣ Create Vector Store
# -----------------------------
vectorstore = FAISS.from_documents(split_docs, embedding_model)


# -----------------------------
# 6️⃣ Manual Retrieval (No RetrievalQA)
# -----------------------------
query = "Give me Eligibility for Refunds?"
retrieved_docs = vectorstore.similarity_search(query, k=2)
context = "\n".join([doc.page_content for doc in retrieved_docs])
print("Retrieved Context:\n", context)

# -----------------------------
# 7️⃣ Call Google GenAI (Gemini)
# -----------------------------
client = genai.Client(api_key=GEMINI_API_KEY)

prompt = f"""
Answer the question using the context below.

Context:
{context}

Question:
{query}
"""

response = client.models.generate_content(
    model=GEMINI_MODEL_NAME,
    contents=prompt
)

print("\nFinal Answer:\n", response.text)