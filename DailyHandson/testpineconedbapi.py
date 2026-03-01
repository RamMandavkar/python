
## pip install pinecone
## https://app.pinecone.io/organizations/-OmYGVgFdDpNCv7UFnjI/projects/ad2262d6-746b-4ec2-88b1-50bb8601a45e/index-quickstart
## PINECONE_API_KEY=pcsk_3dcvXS_BSUMo7FRLcEC67rLAxmC8UP2Gpj3kHFsoknVgqAx2o2o9pYVvSJwJeBh5uKFJ6u
## https://www.pinecone.io/
## https://pastebin.com/px9eYmgM

from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
import time
import os
from dotenv import load_dotenv

load_dotenv()  # loads .env into environment
# Replace with your own keys or use environment variables
PINECONE_API_KEY = os.getenv("pinecone_api_key")

pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "demo-index"

if index_name not in [i.name for i in pc.list_indexes()]:
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

index = pc.Index(index_name)

model = SentenceTransformer("paraphrase-MiniLM-L6-v2")




texts = [
    "AI is transforming healthcare",
    "Robotics in industrial automation",
    "Machine learning in finance",
    "AI for simulation and modeling",
    "Cloud computing basics"
]

for i, text in enumerate(texts):
    embedding = model.encode(text).tolist()

    metadata = {
        "category": "ai" if "AI" in text else "other",
        "created_at": int(time.time()),
        "keywords": text.lower().split()
    }

    index.upsert([
        (f"doc-{i}", embedding, metadata)
    ])
    
    
    
query = "AI in simulations"
query_embedding = model.encode(query).tolist()

results = index.query(
    vector=query_embedding,
    top_k=3,
    include_metadata=True
)

for match in results["matches"]:
    print(match["id"], match["score"])
    print(match["metadata"])
    print("-----")

