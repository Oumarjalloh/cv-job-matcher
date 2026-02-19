from fastapi import FastAPI
from pydantic import BaseModel
from src.index.search import search
from src.ranking.score import final_ranking

app = FastAPI(title="CV Job Matcher API")

class Query(BaseModel):
    cv_text: str
    k: int = 10

@app.post("/match")
def match(q: Query):
    cand = search(q.cv_text, k=50)
    ranked = final_ranking(cand, q.cv_text).head(q.k)
    return ranked[["job_id","title","company","city","level","semantic_score","final_score","rule_details"]].to_dict(orient="records")