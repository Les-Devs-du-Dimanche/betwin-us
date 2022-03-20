from os import sep
from os.path import join
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

def path(relative_path: str) -> str:
    return str(BASE_DIR) + sep + join(*relative_path.split('/'))
