import numpy as np 
from sentence_transformers import SentenceTransformer
from src.config import DEFAULT_EMBED_MODEL 

def get_model(model_name: str = DEFAULT_EMBED_MODEL):
    return SentenceTransformer(model_name)

def embed_texts(texts: list[str], model_name: str = DEFAULT_EMBED_MODEL, batch_size: int = 32) -> np.ndarray:
    model = get_model(model_name)
    emb = model.encode(texts, batch_size, show_progress_bar=True, normalize_embeddings=True)
    return np.asarray(emb, dtype="float32")