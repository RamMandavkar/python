# https://codeshare.io/2jxQPR
## The Case of Aarav and the Golden Trophy
# !pip install faiss-cpu


# Setup
import numpy as np
import faiss
from sklearn.metrics.pairwise import cosine_similarity
import time

np.random.seed(42)

num_students = 120000
dim = 128  # personality fingerprint dimension

student_vectors = np.random.randn(num_students, dim).astype("float32")

# Aarav's index
aarav_index = 12345
aarav_vector = student_vectors[aarav_index]

## Create our First Clue
clue_vector = aarav_vector + 0.01 * np.random.randn(dim).astype("float32")

## Exact Dense Search (Brute Force)
# Compute cosine similarity manually
similarities = cosine_similarity(
    clue_vector.reshape(1, -1),
    student_vectors
)[0]

# Get top 10 most similar students
top_10_indices = np.argsort(-similarities)[:10]

print("Top 10 suspects:", top_10_indices)
print("Is Aarav included?", aarav_index in top_10_indices)

## This is IndexFlat (exact search)
## Sparse Search
# Simulate badge IDs
badge_ids = np.random.randint(10000, 99999, size=num_students)

# Suppose Aarav used badge 57294
badge_ids[aarav_index] = 57294

# Sparse search
matched_indices = np.where(badge_ids == 57294)[0]

print("Badge match:", matched_indices)

# Sparse retrieval = exact filtering.
## Hybrid = Combine Dense + Sparse

# Give badge matches extra score
hybrid_scores = similarities.copy()

# Boost score if badge matches
hybrid_scores[badge_ids == 57294] += 0.5

top_10_hybrid = np.argsort(-hybrid_scores)[:10]

print("Hybrid Top 10:", top_10_hybrid)
print("Is Aarav included?", aarav_index in top_10_hybrid)