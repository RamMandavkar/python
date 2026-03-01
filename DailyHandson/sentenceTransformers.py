## https://codeshare.io/5Ooj7W
## sentenceTransformers.py
## 1. Installing the requirements
# !pip install faiss-cpu
# !pip install sentence-transformers
# !pip install psutil 


## 2. Imports
import os, time, psutil, numpy as np
import faiss
from sentence_transformers import SentenceTransformer
print("FAISS:", faiss.__version__)


# Small toy dataset (each string = one document)
texts = [
    "Document about AI simulations.",
    "Deep learning and neural networks.",
    "Vector databases and similarity search.",
    "Graph-based indexing methods.",
    "Clustering algorithms in machine learning."
]

## Took a model to create embeddings
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

emb = model.encode(texts, convert_to_numpy=True).astype("float32")

##Checking the Embeddings are created right
N, d = emb.shape
print("Documents:", N)
print("Dimension:", d)

## Normalized to calculate Similarity
faiss.normalize_L2(emb)

## Creating a dict of documents
ids = np.arange(N).astype("int64")
id_to_text = {i: texts[i] for i in range(N)}

## Running HNSW

M = 32  # Graph connectivity

hnsw = faiss.IndexHNSWFlat(d, M, faiss.METRIC_INNER_PRODUCT)

hnsw.hnsw.efConstruction = 200
hnsw.hnsw.efSearch = 64

hnsw = faiss.IndexIDMap2(hnsw)
hnsw.add_with_ids(emb, ids)

print("HNSW vectors:", hnsw.ntotal)


















