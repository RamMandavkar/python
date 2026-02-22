# Step 1: Install Packages
# pip install langchain langchain-community langchain-google-genai google-genai faiss-cpu python-dotenv
# ==============================
# 1. Imports
# ==============================
import sys
import os
from dotenv import load_dotenv
from google import genai
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document 
from sentence_transformers import SentenceTransformer
import numpy as np
from langchain.embeddings.base import Embeddings

load_dotenv()  # loads .env into environment
## 1. Setup the API Key
# Replace with your own keys or use environment variables
GEMINI_API_KEY = os.getenv("gemini_api_key")
print("GEMINI_API_KEY:", GEMINI_API_KEY)
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY
GEMINI_MODEL_NAME=os.getenv("gemini_model_name")
client = genai.Client(api_key=GEMINI_API_KEY)
# ==============================
# 2. Load Text File
# ==============================
# Get current working directory
current_dir = os.getcwd()
print("Current Directory: ", current_dir)

# Create full file path
file_path = os.path.join(current_dir, "\\docs\\companypolicy.txt")
print("File Path:", file_path)
loader = TextLoader("python/DailyHandson/docs/companypolicy.txt") # your text file
documents = loader.load()
print("Loaded Documents: ", len(documents))
print("=" * 100)
#sys.exit(0)

# ==============================
# 3. Split Text into Chunks
# ==============================
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

split_docs = text_splitter.split_documents(documents)

print("Total Chunks: ", len(split_docs))

# ---------------------------------------------------
# 4. SentenceTransformer Embedding Wrapper
# ---------------------------------------------------
class SentenceTransformerEmbeddings(Embeddings):
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts):
        return self.model.encode(texts).tolist()

    def embed_query(self, text):
        return self.model.encode(text).tolist()


embedding_model = SentenceTransformerEmbeddings()

# ---------------------------------------------------
# 5. Create Vector Store
# ---------------------------------------------------
vectorstore = FAISS.from_documents(split_docs, embedding_model)

# ---------------------------------------------------
# 6. Advanced Retrieval Function (Manual RAG)
# ---------------------------------------------------
def advanced_retrieve(query, top_k=5):
    print("=" * 100)
    print("----> user query:\n", query)
    # Dense retrieval
    results = vectorstore.similarity_search_with_score(query, k=top_k)
    print("=" * 100)
    print("----> vectorstore results:\n", results)
    # Manual reranking
    query_embedding = np.array(embedding_model.embed_query(query))
    print("=" * 100)
    print("----> vectorstore query_embedding:\n", query_embedding)

    reranked = []
    for doc, _ in results:
        doc_embedding = np.array(
            embedding_model.embed_query(doc.page_content)
        )
        score = np.dot(query_embedding, doc_embedding) / (
            np.linalg.norm(query_embedding) *
            np.linalg.norm(doc_embedding)
        )
        reranked.append((doc, score))

    reranked.sort(key=lambda x: x[1], reverse=True)

    return [doc for doc, _ in reranked[:3]]

# ---------------------------------------------------
# 7. Context Builder
# ---------------------------------------------------
def build_context(docs):
    context = "\n\n".join([doc.page_content for doc in docs])
    print("=" * 100)
    print("----> build_context :\n", context)
    return context

# ---------------------------------------------------
# 8. Query Rewriting (Optional Advanced Step)
# ---------------------------------------------------
def rewrite_query(query):
    prompt = f"Rewrite this query for better document retrieval:\n{query}"
    response = client.models.generate_content(
        model=GEMINI_MODEL_NAME,
        contents=prompt
    )
    print("=" * 100)
    print("----> rewrite_query :\n", response.text)
    return response.text

# ---------------------------------------------------
# 9. Final RAG Pipeline
# ---------------------------------------------------
def advanced_rag_pipeline(user_query):
    
    rewritten_query = rewrite_query(user_query)
    
    retrieved_docs = advanced_retrieve(rewritten_query)
    
    context = build_context(retrieved_docs)    

    final_prompt = f"""
You are an expert assistant.
Answer ONLY from the provided context.

Context:
{context}

Question:
{user_query}
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL_NAME,
        contents=final_prompt
    )
    print("=" * 100)
    print("-----> client.models.generate_content response:\n", response.text)
    return response.text


# ---------------------------------------------------
# 10. Test
# ---------------------------------------------------
if __name__ == "__main__":
    query = "Explain the main topic of the document"
    answer = advanced_rag_pipeline(query)  

