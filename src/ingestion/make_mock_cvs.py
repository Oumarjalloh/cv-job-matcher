import random
import pandas as pd
from src.config import DATA_RAW

SKILLS = ["python","sql","pandas","sklearn","nlp","transformers","bert","faiss","spark","airflow","dbt","aws","docker","kubernetes","fastapi","streamlit"]
LEVELS = ["junior","mid","senior"]
CITIES = ["Paris","Lyon","Remote","Lille","Bordeaux"]

def make_cvs(n=30, seed=7):
    random.seed(seed)
    rows = []
    for i in range(n):
        level = random.choice(LEVELS)
        city = random.choice(CITIES)
        skills = sorted(set(random.sample(SKILLS, k=random.randint(6, 10))))
        years = {"junior": random.randint(0,2), "mid": random.randint(2,5), "senior": random.randint(5,10)}[level]
        text = f"""
        CV MOCK {i}
        Location preference: {city}
        Seniority: {level} ({years} years)
        Skills: {", ".join(skills)}
        Experience: built APIs, worked on data pipelines, wrote tests, deployed models.
        """
        rows.append({"cv_id": f"cv_{i:03d}", "city_pref": city, "level": level, "text": text.strip()})
    return pd.DataFrame(rows)

def main():
    df = make_cvs()
    out = DATA_RAW / "mock_cvs.csv"
    df.to_csv(out, index=False)
    print(f"Saved: {out}")

if __name__ == "__main__":
    main()