from pathlib import Path
import requests


def download_file(url: str, cache_key: str) -> Path:
    out = Path('cache') / cache_key
    if not out.exists():
        out.parent.mkdir(exist_ok=True, parents=True)
        print("download", url)
        r = requests.get(url)
        r.raise_for_status()
        with out.open('wb') as fh:
            for block in r.iter_content(4096):
                fh.write(block)
    return out
