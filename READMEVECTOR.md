## Facebook AI Similarity Search (FAISS) 

    FAISS (Facebook AI Similarity Search) is a library for fast similarity search and clustering of vectors. 
    It is widely used in vector databases, embeddings search, semantic search, and RAG systems.

## Approximate Nearest Neighbor (ANN)

Approximate Nearest Neighbor (ANN) is a technique used to quickly find similar vectors (embeddings) in a large dataset. It is widely used in vector databases, RAG systems, semantic search, and recommendation systems.

Instead of finding the exact nearest vectors, ANN finds very close matches much faster.    

# Why ANN is Needed
    When working with embeddings:
    1 document → 1 vector
    1 million documents → 1 million vectors
    Finding nearest vectors using exact search is slow:
    ANN reduces search time dramatically.