🧠 CV ↔ Job Matcher (NLP + Semantic Ranking)
Moteur de matching intelligent entre CV et offres d’emploi basé sur des embeddings SBERT + recherche sémantique FAISS + ranking hybride (ML + règles métier).
Projet orienté produit data, avec métriques de ranking, UI interactive et considérations RGPD.

🚀 Objectif
Permettre à un candidat d’uploader son CV et d’obtenir :
🔎 Les offres les plus pertinentes
📊 Un score de matching
🧠 Une explication du score

🏗️ Architecture
cv-job-matcher/
│
├── app/
│   └── streamlit_app.py
│
├── src/
│   ├── parsing/
│   ├── embeddings/
│   ├── index/
│   ├── ranking/
│   ├── evaluation/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│   ├── faiss.index
│   └── meta.pkl
│
├── requirements.txt
└── README.md

🔬 Stack technique

Python 3.10+
Sentence-Transformers (SBERT)
FAISS
Pandas / NumPy
Streamlit
Scikit-learn
Ranking metrics (Precision@K, NDCG)

📦 Installation (Windows)
1️⃣ Cloner le repo

git clone <repo_url>
cd cv-job-matcher

2️⃣ Créer un environnement virtuel

python -m venv .venv
.venv\Scripts\activate

3️⃣ Installer les dépendances

pip install -r requirements.txt

python -m src.ingestion.load_jobs

python -m src.ingestion.make_mock_cvs

python -m src.index.build_index

python -m src.eval.make_qrels

python -m src.eval.evaluate

streamlit run app\streamlit_app.py


Dans un autre terminal (même venv) : 
uvicorn api.main:app --reload

Ouvre : 
http://127.0.0.1:8000/docs

Test rapide : copie/colle un texte de CV dans /match.

🧠 Construction de l’index sémantique
python -m src.index.build_index


Cela :
Charge les offres
Génère les embeddings SBERT
Crée l’index FAISS
Sauvegarde faiss.index + meta.pkl

📊 Évaluation du ranking
python -m src.evaluation.evaluate

Métriques calculées :
Precision@K
Recall@K
NDCG@K

🖥️ Lancer l’application
Depuis la racine du projet :
streamlit run app/streamlit_app.py
Puis :
Upload d’un CV (.txt ou .pdf)
Top offres affichées
Score + explication

🧠 Modèle utilisé
SBERT : all-MiniLM-L6-v2
Embeddings normalisés
Similarité cosinus via FAISS

🏆 Scoring final

Score hybride :

Score final =
    α * Similarité sémantique
  + β * Matching localisation
  + γ * Matching seniorité
  + δ * Matching salaire


Permet d’avoir :
ML (recherche sémantique)
Règles métier (logique produit)

📈 Exemple de métriques
Metric	@5
Precision@5	0.82
NDCG@5	0.88


🔐 RGPD & Données
CV anonymisés
Aucune donnée sensible stockée
Pas de stockage permanent des fichiers uploadés
Logs anonymisés

📹 Démo attendue (2–3 min)
Montrer :
Upload CV
Résultats top 5
Score + explication
Métriques d’évaluation
