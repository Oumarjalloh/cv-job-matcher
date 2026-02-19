import pandas as pd
import faiss
from src.config import DATA_RAW, FAISS_DIR
from src.embeddings.embed import embed_texts

def main():
    FAISS_DIR.mkdir(parents=True, exist_ok=True)

    jobs = pd.read_csv(DATA_RAW / "jobs.csv")
    docs = (jobs["title"].fillna("") + "\n" + jobs["description"].fillna("")).tolist()

    X = embed_texts(docs)
    d = X.shape[1]

    index = faiss.IndexFlatIP(d)
    index.add(X)

    faiss.write_index(index, str(FAISS_DIR / "jobs.index"))
    jobs.to_parquet(FAISS_DIR / "jobs.parquet", index=False)
    print("Saved FAISS index + jobs metadata.")


if __name__ == "__main__":
    main()