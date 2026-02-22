# python
### Complete RAG(Retrieval-Augmented Generation) Architecture with Chunking
            Raw Documents
                ↓
            Chunking
                ↓
            Embeddings (vectorize chunks)
                ↓
            Vector Database (store vectors)
                ↓
            User Query
                ↓
            Query Embedding
                ↓
            Similarity Search (cosine similarity)
                ↓
            Top K relevant chunks
                ↓
            LLM + Context
                ↓
            Final Answer

### Complete End-to-End RAG(Retrieval-Augmented Generation) Flow Diagram 
                ┌──────────────────────┐
                │   External Data      │
                └──────────┬───────────┘
                           ↓
                ┌──────────────────────┐
                │  Loader + Splitter   │
                └──────────┬───────────┘
                           ↓
                ┌──────────────────────┐
                │   Embedding Model    │
                └──────────┬───────────┘
                           ↓
                ┌──────────────────────┐
                │    Vector Store      │
                └──────────┬───────────┘
                           ↓
              User Query → Query Embedding
                           ↓
                ┌──────────────────────┐
                │  Similarity Search   │
                └──────────┬───────────┘
                           ↓
                    Retrieved Context
                           ↓
                ┌──────────────────────┐
                │       LLM            │
                └──────────┬───────────┘
                           ↓
                     Final Answer