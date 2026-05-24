import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(fmt)

    arquivo = RotatingFileHandler(
        LOG_DIR / "app.log",
        mode="a",
        maxBytes=5 * 1024 * 1024,
        backupCount=3
    )
    arquivo.setLevel(logging.INFO)
    arquivo.setFormatter(fmt)

    logger.addHandler(console)
    logger.addHandler(arquivo)

    return logger