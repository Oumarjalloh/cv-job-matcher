import random
import pandas as pd
from src.config import DATA_RAW

CITIES = ["Paris", "Lyon", "Marseille", "Lille", "Nantes", "Bordeaux", "Toulouse", "Remote"]
LEVELS = ["junior", "mid", "senior"]
ROLES = [
    ("Data Scientist", ["python", "sql", "ml", "sklearn", "pandas", "nlp"]),
    ("Data Engineer", ["python", "sql", "spark", "airflow", "dbt", "aws"]),
    ("ML Engineer", ["python", "pytorch", "docker", "kubernetes", "mlops", "api"]),
    ("Software Engineer", ["python", "java", "react", "docker", "git", "tests"]),
    ("NLP Engineer", ["python", "transformers", "bert", "faiss", "retrieval", "rag"]),
]

def make_jobs(n=400, seed=42):
    random.seed(seed)
    rows = []
    for i in range(n):
        role, base_skills = random.choice(ROLES)
        level = random.choice(LEVELS)
        city = random.choice(CITIES)
        salary_min = random.choice([35, 40, 45, 50, 55, 60]) * 1000
        salary_max = salary_min + random.choice([5, 10, 15]) * 1000

        skills = random.sample(base_skills, k=min(len(base_skills), random.randint(4, 6)))
        extra = random.sample(["gcp", "azure", "fastapi", "streamlit", "faiss", "linux", "ci/cd"], k=random.randint(0, 3))
        skills = sorted(set(skills + extra))

        desc = f"We are hiring a {level} {role}. Skills: {', '.join(skills)}. Location: {city}. Salary: {salary_min}-{salary_max}."
        rows.append({
            "job_id": f"job_{i:04d}",
            "title": f"{role} ({level})",
            "company": f"Company_{random.randint(1, 80)}",
            "city": city,
            "level": level,
            "salary_min": salary_min,
            "salary_max": salary_max,
            "skills": ", ".join(skills),
            "description": desc,
        })
    return pd.DataFrame(rows)

def main():
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    df = make_jobs()
    out = DATA_RAW / "jobs.csv"
    df.to_csv(out, index=False)
    print(f"Saved: {out} ({len(df)} rows)")

if __name__ == "__main__":
    main()