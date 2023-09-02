from pathlib import Path

from loguru import logger

LOG_DIR = Path(__file__).resolve().parent.parent / 'log'

if not LOG_DIR.exists():
    LOG_DIR.mkdir()

logger.add(
    LOG_DIR / 'error.log',
    rotation='23:30',
    retention='5 days',
)
