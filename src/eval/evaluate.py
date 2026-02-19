import json
import pandas as pd
from ranx import Qrels, Run, evaluate
from src.config import DATA_RAW, REPORTS
from src.index.search import search
from src.ranking.score import final_ranking

def main():
    qrels = Qrels.from_dict(json.loads((REPORTS / "qrels.json").read_text(encoding="utf-8")))
    cvs = pd.read_csv(DATA_RAW / "mock_cvs.csv")

    run_dict = {}
    for _, cv in cvs.iterrows():
        qid = cv["cv_id"]
        cand = search(cv["text"], k=50)
        ranked = final_ranking(cand, cv["text"]).head(50)
        run_dict[qid] = {row["job_id"]: float(row["final_score"]) for _, row in ranked.iterrows()}

    run = Run.from_dict(run_dict)
    metrics = evaluate(qrels, run, ["precision@10", "ndcg@10", "mrr@10"])

    out = REPORTS / "ranking_metrics.json"
    out.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(metrics)
    print(f"Saved {out}")

if __name__ == "__main__":
    main()