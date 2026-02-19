import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)


import streamlit as st
from pathlib import Path
from src.parsing.cv_extract import read_cv
from src.index.search import search
from src.ranking.score import final_ranking
from src.ranking.explain import explain_match
from src.utils.logging_setup import setup_logger

logger = setup_logger()

st.set_page_config(page_title="CV ↔ Job Matcher", layout="wide")
st.title("🔎 Matching CV ↔ Offres (Semantic Search + Ranking)")

uploaded = st.file_uploader("Upload ton CV (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
k = st.slider("Nombre d'offres à afficher", 5, 30, 10)

if uploaded:
    Path("runs").mkdir(exist_ok=True)
    tmp_path = f"runs/{uploaded.name}"
    with open(tmp_path, "wb") as f:
        f.write(uploaded.getbuffer())

    cv_text = read_cv(tmp_path)
    st.subheader("Extrait du CV (debug)")
    st.text_area("CV text", cv_text[:2000], height=180)

    with st.spinner("Recherche sémantique + scoring..."):
        candidates = search(cv_text, k=50)
        ranked = final_ranking(candidates, cv_text).head(k)

    logger.info(f"query_len={len(cv_text)} results={len(ranked)}")

    st.subheader("Top offres")
    for i, row in ranked.iterrows():
        job_text = f"{row['title']}\n{row['description']}"
        exp = explain_match(cv_text, job_text, row["rule_details"])

        with st.expander(f"#{i+1} {row['title']} — score={row['final_score']:.3f} — {row['company']} ({row['city']})"):
            st.write(row["description"])
            st.json({
                "semantic_score": float(row["semantic_score"]),
                "final_score": float(row["final_score"]),
                "explanations": exp
            })