from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

print("= " * 65)
print("FAISS with Embeddings")
## FAISS with Embeddings
texts = [
    "Apple is a fruit",
    "Dog is an animal",
    "Car is a vehicle",
    "Cat is a pet"
]
embeddings = model.encode(texts).astype('float32')

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)
# Search
query = model.encode(["pet animal"]).astype('float32')
distances, indices = index.search(query, 2)
# Print results
for i in indices[0]:
    print(texts[i])

print("= " * 65)
print("Cosine Similarity in FAISS")
## Cosine Similarity in FAISS
faiss.normalize_L2(embeddings)
index = faiss.IndexFlatIP(dimension)
index.add(embeddings)
# Search
query = model.encode(["pet animal"]).astype('float32')
faiss.normalize_L2(query)
distances, indices = index.search(query, 2)
# Print results
for i in indices[0]:
    print(texts[i])

print("= " * 65)
print("FAISS in RAG Architecture")
##  FAISS in RAG Architecture
query = "What is photosynthesis?"

query_vector = model.encode([query]).astype('float32')
distances, indices = index.search(query_vector, 3)
results = [texts[i] for i in indices[0]]
print(results)    


print("= " * 65)
print("Large Dataset – IVF Index (ANN)")

# Large Dataset – IVF Index (ANN)
# ??

