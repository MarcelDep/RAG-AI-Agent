import json
import time
from pathlib import Path

import requests

URL = "https://api2.openreview.net/notes/search"
INVITATION = "ICLR.cc/2024/Conference/-/Submission"
TERM = "reinforcement learning"
LIMIT = 100

OUTPUT = Path("data/iclr2024_transformer.jsonl")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

session = requests.Session()
session.headers.update({
    "User-Agent": "RAG-AI-Agent/1.0 (research data collection)"
})

offset = 0
total = None
downloaded = 0

with OUTPUT.open("w", encoding="utf-8") as f:
    while total is None or offset < total:
        params = {
            "invitation": INVITATION,
            "term": TERM,
            "limit": LIMIT,
            "offset": offset,
        }

        response = session.get(URL, params=params, timeout=30)

        if response.status_code == 403:
            raise RuntimeError(
                "OpenReview wymaga weryfikacji antybotowej. "
                "Przerwano pobieranie."
            )

        response.raise_for_status()
        data = response.json()
        notes = data.get("notes", [])
        total = data.get("count", len(notes))

        if not notes:
            break

        for note in notes:
            f.write(json.dumps(note, ensure_ascii=False) + "\n")

        downloaded += len(notes)
        offset += len(notes)

        print(f"Pobrano {downloaded} / {total}")

        if offset < total:
            time.sleep(0.2)

print(f"Zapisano {downloaded} rekordów do {OUTPUT}")