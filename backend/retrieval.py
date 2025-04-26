import faiss
import numpy as np

# Create a simple FAISS index
def create_faiss_index(embedding_dim):
    index = faiss.IndexFlatL2(embedding_dim)  # L2 = distance
    return index

# Add embeddings to the index
def add_to_index(index, embeddings):
    index.add(np.array(embeddings))

# Search for nearest neighbors
def search_index(index, query_embedding, top_k=5):
    distances, indices = index.search(np.array([query_embedding]), top_k)
    return distances[0], indices[0]
