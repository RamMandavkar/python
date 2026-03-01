## pip install nltk sentence-transformers scikit-learn
## https://codeshare.io/5eplxK
## https://docs.langchain.com/oss/python/integrations/splitters

import re
import nltk
nltk.download('punkt_tab')
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Sample input text
sample_text = """
Section 1: Loan Eligibility
To qualify for a personal loan, the customer must be between 21 and 60 years old, have a minimum salary of ₹25,000, and a credit score above 700.

Section 2: Disbursal and Timelines
Loan disbursal typically occurs within 48 hours of approval. Delays can occur due to incomplete documentation.

Section 3: EMI Defaults
If the customer misses 2 or more EMIs, penalties apply. Further defaults may lead to legal action or freezing of accounts.

Section 4: Foreclosure
Customers can foreclose their loan after 6 EMIs have been paid. A foreclosure fee of 2% is applicable.
"""

def fixed_size_chunking(text, chunk_size=300, overlap=50):
    """
    Split text into fixed-size chunks with optional overlap (measured in tokens).
    """
    tokens = text.split()
    chunks = []
    start = 0
    while start < len(tokens):
        end = start + chunk_size
        chunk = ' '.join(tokens[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks
    
def hierarchical_chunking(text):
    """
    Split document using structured section headers (e.g., "Section 1:", "Section 2:").
    """
    sections = re.split(r'\n(?=Section \d+:)', text.strip())
    return [sec.strip() for sec in sections if sec.strip()]
    
    
def semantic_chunking(text, threshold=0.75):
    """
    Group nearby sentences based on semantic similarity (using cosine similarity).
    """
    model = SentenceTransformer('all-MiniLM-L6-v2')
    sentences = sent_tokenize(text)
    embeddings = model.encode(sentences)

    chunks = []
    current_chunk = [sentences[0]]
    for i in range(1, len(sentences)):
        sim = cosine_similarity([embeddings[i]], [embeddings[i-1]])[0][0]
        if sim >= threshold:
            current_chunk.append(sentences[i])
        else:
            chunks.append(' '.join(current_chunk))
            current_chunk = [sentences[i]]
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks
    
    
def display_chunks(chunks, title):
    print(f"\n{title} -- Total Chunks: {len(chunks)}")
    for i, chunk in enumerate(chunks):
        print(f"\n--- Chunk {i+1} ---\n{chunk}")  
        
        

fixed_chunks = fixed_size_chunking(sample_text, chunk_size=40, overlap=10)
hierarchical_chunks = hierarchical_chunking(sample_text)
semantic_chunks = semantic_chunking(sample_text, threshold=0.75)

display_chunks(fixed_chunks, "Fixed-Size Chunking")
display_chunks(hierarchical_chunks, "Hierarchical Chunking")
display_chunks(semantic_chunks, "Semantic Chunking")

## If Resource punkt_tab not found. error occurs
#import nltk
#nltk.download('punkt_tab')