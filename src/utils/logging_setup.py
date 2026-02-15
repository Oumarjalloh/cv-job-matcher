from loguru import logger
from src.config import LOGS

def setup_logger():
    LOGS.mkdir(parents=True, exist_ok=True)
    logger.add(LOGS / "app.log", rotation="10 MB", retention="14 days")
    return logger