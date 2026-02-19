from rapidfuzz import fuzz

def explain_match(cv_text: str, job_text: str, rule_details: dict) -> dict:
    overlap_hint = fuzz.partial_ratio(cv_text.lower(), job_text.lower())
    return {"rules": rule_details, "text_overlap_hint": overlap_hint}