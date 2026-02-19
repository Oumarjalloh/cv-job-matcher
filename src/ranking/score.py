import re
import pandas as pd

LEVEL_ORDER = {"junior": 0, "mid": 1, "senior": 2}

def extract_preferences(cv_text: str) -> dict:
    t = cv_text.lower()
    city = None
    m = re.search(r"location preference:\s*([a-z]+)", t)
    if m:
        city = m.group(1).capitalize()

    level = None
    m = re.search(r"seniority:\s*(junior|mid|senior)", t)
    if m:
        level = m.group(1)

    salary = None
    m = re.search(r"salary expectation:\s*(\d+)", t)
    if m:
        salary = int(m.group(1))

    return {"city_pref": city, "level": level, "salary_expectation": salary}

def rule_score(job_row: pd.Series, prefs: dict) -> tuple[float, dict]:
    bonus = 0.0
    details = {}

    # Location
    if prefs["city_pref"]:
        if job_row["city"] == "Remote" and prefs["city_pref"] != "Remote":
            bonus += 0.05
            details["location"] = "+0.05 remote ok"
        elif job_row["city"] == prefs["city_pref"]:
            bonus += 0.10
            details["location"] = "+0.10 city match"
        else:
            bonus -= 0.03
            details["location"] = "-0.03 city mismatch"

    # Seniority
    if prefs["level"]:
        cv_l = LEVEL_ORDER[prefs["level"]]
        job_l = LEVEL_ORDER.get(str(job_row["level"]).lower(), 1)
        gap = job_l - cv_l
        if gap >= 2:
            bonus -= 0.12
            details["seniority"] = "-0.12 too senior"
        elif gap == 1:
            bonus -= 0.05
            details["seniority"] = "-0.05 slightly senior"
        else:
            bonus += 0.03
            details["seniority"] = "+0.03 ok"

    # Salary (optional)
    if prefs["salary_expectation"]:
        if job_row["salary_max"] >= prefs["salary_expectation"]:
            bonus += 0.05
            details["salary"] = "+0.05 meets expectation"
        else:
            bonus -= 0.08
            details["salary"] = "-0.08 below expectation"

    return bonus, details

def final_ranking(candidates: pd.DataFrame, cv_text: str, alpha: float = 0.85) -> pd.DataFrame:
    prefs = extract_preferences(cv_text)
    finals = []
    details_list = []
    for _, r in candidates.iterrows():
        b, det = rule_score(r, prefs)
        final = alpha * float(r["semantic_score"]) + (1 - alpha) * (float(r["semantic_score"]) + b)
        finals.append(final)
        details_list.append(det)

    out = candidates.copy()
    out["final_score"] = finals
    out["rule_details"] = details_list
    return out.sort_values("final_score", ascending=False).reset_index(drop=True)