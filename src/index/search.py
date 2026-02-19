import pandas as pd
import faiss
from src.config import FAISS_DIR
from src.embeddings.embed import embed_texts

def load():
    index = faiss.read_index(str(FAISS_DIR / "jobs.index"))
    jobs = pd.read_parquet(FAISS_DIR / "jobs.parquet")
    return index, jobs

def search(query_text: str, k: int = 20):
    index, jobs = load()
    q = embed_texts([query_text])
    scores, idx = index.search(q, k)
    scores = scores[0].tolist()
    idx = idx[0].tolist()
    res = jobs.iloc[idx].copy()
    res["semantic_score"] = scores
    return res.reset_index(drop=True)