from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
MODELS = ROOT / "models"
FAISS_DIR = MODELS / "faiss"
RUNS = ROOT / "runs"
LOGS = RUNS / "logs"
REPORTS = RUNS / "reports"

DEFAULT_EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"