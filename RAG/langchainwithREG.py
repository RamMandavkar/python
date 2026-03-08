# LSESRG = Let Smart Engineers Solve RAG Gracefully
# L=Load  S=Split E=Embbed S=Store R=Retrieve G=Generate

# pip install sentence-transformers google-genai beautifulsoup4 rank_bm25
# pip install -U langchain-community unstructured bs4 langchain-text-splitters pinecone langchain-google-genai langchain-pinecone pinecone-text
# https://www.firecrawl.dev/
# https://serpapi.com/
# https://codeshare.io/5w8lYj

from pathlib import Path
import time, os, re, json
from typing import List, Dict, Tuple
from bs4 import BeautifulSoup
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from google import genai
from dotenv import load_dotenv
import os

# Load variables from .env into os.environ
load_dotenv()

PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]


import os, time
from pinecone import Pinecone

pc = Pinecone(api_key=PINECONE_API_KEY)

INDEX_NAME = "coffeeindex"

# Delete the index if it exists
if INDEX_NAME in pc.list_indexes().names():
    print(f"Deleting index: {INDEX_NAME} ...")
    pc.delete_index(INDEX_NAME)
    # optional: poll until it disappears
    for _ in range(30):
        if INDEX_NAME not in pc.list_indexes().names():
            print("✅ Deleted.")
            break
        time.sleep(1)
else:
    print(f"Index '{INDEX_NAME}' does not exist.")

from langchain_community.document_loaders import DirectoryLoader, UnstructuredHTMLLoader

current_dir = os.getcwd()
print("Current Directory:", current_dir)
#file_path = os.path.join(current_dir, "python/DailyHandson/docs/pdfreader.pdf")
#print("Current Directory:", current_dir)
# Load all HTML files from a folder into LangChain Documents
loader = DirectoryLoader(
    "python/RAG/coffee_pages",
    glob="**/*.html",
    loader_cls=UnstructuredHTMLLoader
)
docs = loader.load()
print("Loaded:", len(docs))

# pip install -U sentence-transformers

# pip install -U sentence-transformers

# pip install -U sentence-transformers

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
# Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)
print("Chunks:", len(chunks))

# Define embeddings
embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-MiniLM-L6-v2"
)
    
from pathlib import Path
import os
from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

INDEX_NAME = "coffeeindex"
REGION     = "us-east-1"
EMBED_DIM  = 384  # Gemini embeddings

# (Re)create
if INDEX_NAME in pc.list_indexes().names():
    pc.delete_index(INDEX_NAME)
pc.create_index(
    name=INDEX_NAME,
    dimension=EMBED_DIM,
    metric="cosine",
    spec=ServerlessSpec(cloud="aws", region=REGION),
)
idx = pc.Index(INDEX_NAME)
idx


from langchain_community.embeddings import HuggingFaceEmbeddings

# MiniLM-L6-v2 → 384-dim
embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-MiniLM-L6-v2"
)

# Sanity: check embedding size
vec = embedding.embed_documents(["hello world"])[0]
print("HF embed dim:", len(vec))  # expect 384


# pip install --upgrade langchain-pinecone
from langchain_pinecone import PineconeVectorStore

vectorstore_from_docs = PineconeVectorStore.from_documents(
    chunks,      # your split LangChain Documents
    embedding=embedding,    # HF embedder (384)
    index_name=INDEX_NAME,
    text_key="text",
)


print(idx.describe_index_stats())  # total_vector_count should reflect your inserts


vectorstore = PineconeVectorStore(index_name=INDEX_NAME, embedding=embedding)
query = "What is Ashwagandha coffee?"
vectorstore.similarity_search(query)


# pip install -U pinecone langchain-pinecone langchain-community sentence-transformers

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-MiniLM-L6-v2"
)

vectorstore = PineconeVectorStore(
    index_name="coffeeindex",
    embedding=embedding,
    text_key="text",
)

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 8}
)

docs = retriever.invoke("What is turmeric coffee?")
print(len(docs))



# Search with automatic Keyword detection
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains.query_constructor.schema import AttributeInfo
from langchain_classic.retrievers import SelfQueryRetriever


# 1. Define metadata schema fields
metadata_field_info = [
    AttributeInfo(
        name="heading_keywords",
        description="Main topics or section headings in the document (e.g., Turmeric, Ashwagandha, Saffron, Benefits, Side Effects)",
        type="string or list[string]",
    ),
    AttributeInfo(
        name="department",
        description="Business department such as HR, Finance, Marketing, or Support",
        type="string",
    ),
]

# 2. Gemini LLM for query rewriting + filter extraction

llm_filter = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.environ["GEMINI_API_KEY"],  # 👈 force API key auth
    temperature=0,
)


# 3. Build a SelfQueryRetriever
retriever = SelfQueryRetriever.from_llm(
    llm=llm_filter,
    vectorstore=vectorstore,   # your Pinecone LangChain vectorstore
    document_contents="Knowledge base about coffee, herbs, and health benefits.",
    metadata_field_info=metadata_field_info,
    enable_limit=True,         # allow Gemini to set 'k' dynamically
)

# 4. Example query — Gemini auto-adds filter (e.g. heading_keywords="turmeric")
query = "Ashwagandha?"
docs = retriever.invoke(query)

print(f"\nSelfQueryRetriever returned {len(docs)} docs")
for d in docs[:5]:
    print("-", d.metadata.get("headings"), "| chunk:", d.metadata.get("chunk_id"))



