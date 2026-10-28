import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import openreview

VENUES = {
    "iclr2024": "ICLR.cc/2024/Conference",
    "neurips2024": "NeurIPS.cc/2024/Conference",
}
BASE = "https://api2.openreview.net"
LIMIT = 100


def make_client():
    user = os.environ.get("OPENREVIEW_USERNAME")
    pw = os.environ.get("OPENREVIEW_PASSWORD")
    if not user or not pw:
        sys.exit("Ustaw OPENREVIEW_USERNAME i OPENREVIEW_PASSWORD")
    return openreview.api.OpenReviewClient(baseurl=BASE, username=user, password=pw)


def get_batch(client, inv, offset, tries=5):
    for i in range(tries):
        try:
            return client.get_notes(
                invitation=inv, details="replies", limit=LIMIT, offset=offset
            )
        except Exception as e:
            print(f"błąd (próba {i + 1}/{tries}):", str(e)[:200])
            time.sleep(2 ** i)
    raise RuntimeError(f"Nie udało się pobrać offset={offset}")


def fetch(name, max_notes=None):
    client = make_client()
    venue_id = VENUES[name]
    group = client.get_group(venue_id)
    sub_name = group.content["submission_name"]["value"]
    inv = f"{venue_id}/-/{sub_name}"
    print("invitation:", inv)

    stamp = datetime.now(timezone.utc)
    suffix = f"_sample{max_notes}" if max_notes else ""
    base = Path(f"data/raw/{name}_{stamp:%Y%m%d}{suffix}")
    base.parent.mkdir(parents=True, exist_ok=True)

    n, offset = 0, 0
    with open(f"{base}.jsonl", "w", encoding="utf-8") as f:
        while max_notes is None or n < max_notes:
            notes = get_batch(client, inv, offset)
            if not notes:
                break
            if max_notes is not None:
                notes = notes[: max_notes - n]
            for note in notes:
                rec = note.to_json()
                rec["details"] = note.details
                rec["number"] = note.number
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            n += len(notes)
            offset += len(notes)
            print(name, n)
            if len(notes) < LIMIT:
                break
            time.sleep(0.5)

    with open(f"{base}.meta.json", "w", encoding="utf-8") as f:
        json.dump({
            "venue": venue_id,
            "invitation": inv,
            "api": BASE,
            "logged_in": True,
            "fetched_at": stamp.isoformat(),
            "n_submissions": n,
            "max_notes": max_notes,
        }, f, indent=2)
    print("zapisano:", base)


if __name__ == "__main__":
    name = sys.argv[1]
    max_notes = int(sys.argv[2]) if len(sys.argv) > 2 else None
    fetch(name, max_notes)