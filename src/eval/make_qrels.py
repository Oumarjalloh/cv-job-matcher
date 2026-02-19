import pandas as pd
from src.config import DATA_RAW, REPORTS

def relevance(cv_text: str, job_row: pd.Series) -> int:
    cv = cv_text.lower()
    skills = str(job_row["skills"]).lower().split(",")
    hit = sum(1 for s in skills if s.strip() in cv)
    if hit >= 4:
        return 2
    if hit >= 2:
        return 1
    return 0

def main():
    REPORTS.mkdir(parents=True, exist_ok=True)
    cvs = pd.read_csv(DATA_RAW / "mock_cvs.csv")
    jobs = pd.read_csv(DATA_RAW / "jobs.csv")

    qrels = {}
    for _, cv in cvs.iterrows():
        qid = cv["cv_id"]
        qrels[qid] = {}
        for _, job in jobs.iterrows():
            rel = relevance(cv["text"], job)
            if rel > 0:
                qrels[qid][job["job_id"]] = rel

    import json
    out = REPORTS / "qrels.json"
    out.write_text(json.dumps(qrels, indent=2), encoding="utf-8")
    print(f"Saved {out}")

if __name__ == "__main__":
    main()