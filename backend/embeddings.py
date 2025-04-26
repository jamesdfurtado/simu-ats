from sentence_transformers import SentenceTransformer

# Load MiniLM model once
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_text(text):
    """Embed text into a vector."""
    return embedding_model.encode(text, normalize_embeddings=True)
