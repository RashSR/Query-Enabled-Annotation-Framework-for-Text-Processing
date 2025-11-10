import warnings
import urllib3
warnings.simplefilter('ignore', category=UserWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import requests
from pathlib import Path
from tqdm import tqdm

MODEL_URL = "https://github.com/explosion/spacy-models/releases/download/de_core_news_lg-3.8.0/de_core_news_lg-3.8.0-py3-none-any.whl"
MODEL_FOLDER = Path("models")
MODEL_FILE = MODEL_FOLDER / "de_core_news_lg-3.8.0-py3-none-any.whl"

MODEL_FOLDER.mkdir(exist_ok=True)

if MODEL_FILE.exists():
    print(f"Model already downloaded: {MODEL_FILE}")
else:
    print(f"Downloading spaCy model to {MODEL_FILE} ...")
    resp = requests.get(MODEL_URL, stream=True, verify=False)  # Optional: verify=False skips SSL cert check
    total = int(resp.headers.get("content-length", 0))
    with open(MODEL_FILE, "wb") as f, tqdm(total=total, unit="B", unit_scale=True, desc="Downloading") as pbar:
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(len(chunk))
    print("Download complete!")
