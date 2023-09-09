from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / 'data'
CACHE_DIR = DATA_DIR / 'cache'
WATCH_LIST_DIR = DATA_DIR / 'watch_list'
CACHE_DIR.mkdir(exist_ok=True, parents=True)
WATCH_LIST_DIR.mkdir(exist_ok=True, parents=True)
