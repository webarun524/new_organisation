import logging
from pathlib import Path

YELLOW = "\033[0;33m"
RESET = "\033[0m"


class YellowFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        base = super().format(record)
        return f"{YELLOW}{base}{RESET}"


def _ensure_log_setup(log_path: Path, level: int = logging.INFO):
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("e2e")
    if not logger.handlers:
        logger.setLevel(level)
        fh = logging.FileHandler(log_path, encoding="utf-8")
        fmt = YellowFormatter("%(asctime)s %(levelname)-7s %(name)s: %(message)s")
        fh.setFormatter(fmt)
        logger.addHandler(fh)
        ch = logging.StreamHandler()
        ch.setFormatter(fmt)
        logger.addHandler(ch)
    return logger


def get_logger(name: str | None = None):
    base = Path(__file__).resolve().parents[2]
    log_dir = base / "reports"
    log_file = log_dir / "e2e-tests.log"
    logger = _ensure_log_setup(log_file)
    return logger.getChild(name) if name else logger
