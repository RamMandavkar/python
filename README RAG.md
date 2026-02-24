# python
### Word2Vec is a neural-network method that converts words into numerical vectors (embeddings) 
    so that words with similar meanings have similar vectors.

### Doc2Vec is an algorithm used to convert entire documents (paragraphs or sentences) into fixed-length numeric vectors (embeddings). 
    It is an extension of Word2Vec, designed to represent documents instead of words.

### ELMo (Embeddings from Language Models) is a deep contextual word embedding method. Unlike Word2Vec or GloVe (fixed embeddings), 
    ELMo creates different embeddings for the same word depending on context.

### GloVe (Global Vectors for Word Representation) is a method for creating word embeddings (numerical vectors representing word meaning).
    It is based on global word co-occurrence statistics from a large text corpus.
    Unlike SBERT or BERT, GloVe produces embeddings for individual words (not sentences).

### BERT (Bidirectional Encoder Representations from Transformers) is a Transformer Encoder model designed to understand language context.
    Goal of BERT:
        Understand relationships between words in a sentence.

### SBERT modifies BERT to create sentence embeddings.
    Goal of SBERT:
        Convert sentences → vectors → fast similarity search.

### FastText is a word-embedding technique developed by Facebook AI Research. It improves on Word2Vec by representing words using character n-grams,
    which helps handle misspelled words, rare words, and unknown words (OOV).
    FastText converts words or sentences → numerical vectors (embeddings) used in NLP tasks like search, classification, and similarity.        

### The fundamental difference between Word2Vec and BERT lies in context.
    Word2Vec generates static (context-free) embeddings, meaning a word always gets the exact same vector representation regardless of how it is used. 
    BERT generates dynamic (contextualized) embeddings, meaning a word's vector representation changes depending on the surrounding words in the specific sentence

### Parametric
    Parametric methods assume that the data follows a specific, known underlying distribution (most commonly, the normal or Gaussian distribution). In these models, the form of the model is strictly defined, and you only need to learn a fixed set of parameters from the data.

    Non-Parametric
    Non-parametric methods do not assume the data follows any specific distribution (they are often called "distribution-free"). In machine learning, this doesn't mean they have no parameters; rather, it means the number of parameters is not fixed and can grow as the amount of data increases

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