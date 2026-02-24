## pip install sentence-transformers
from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')
sentences = [
    "I love machine learning",
    "I enjoy studying AI",
    "The sky is blue",
    "I love machine learning",
    "Man bites dog",
    "dog bites Man"
]

embeddings = model.encode(sentences)
similarity = util.cos_sim(embeddings[0], embeddings[1])
print(similarity) # tensor([[0.5396]])
sim = cosine_similarity([embeddings[0]], [embeddings[1]])
print(sim) # [[0.5396]]
similarity = util.cos_sim(embeddings[0], embeddings[2])
print(similarity) # tensor([[0.1234]])
sim = cosine_similarity([embeddings[0]], [embeddings[2]])
print(sim) # [[0.1234]]
similarity = util.cos_sim(embeddings[1], embeddings[2])
print(similarity) # tensor([[0.0987]])
sim = cosine_similarity([embeddings[1]], [embeddings[2]])
print(sim) # [[0.0987]]
similarity = util.cos_sim(embeddings[0], embeddings[3])
print(similarity) 
sim = cosine_similarity([embeddings[0]], [embeddings[3]])
print(sim) 
sim = cosine_similarity([embeddings[4]], [embeddings[5]])
print("DOG ->", sim) 

# ~0.1 to 0.3 → Not similar
# ~0.5 to 0.8  → similar
# ~0.8 to 0.9  → Very similar
# ~0.9 to 1  → Very similar/duplicate
