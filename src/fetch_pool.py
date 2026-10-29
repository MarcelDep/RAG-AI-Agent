import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from fetch_openreview import VENUES, BASE, make_client


def fetch_pool(name):
    client = make_client()
    venue_id = VENUES[name]
    sub_name = client.get_group(venue_id).content["submission_name"]["value"]
    inv = f"{venue_id}/-/{sub_name}"
    notes = client.get_all_notes(invitation=inv)

    stamp = datetime.now(timezone.utc)
    base = Path(f"data/raw/{name}_pool_{stamp:%Y%m%d}")
    with open(f"{base}.jsonl", "w", encoding="utf-8") as f:
        for n in notes:
            rec = n.to_json()
            rec["number"] = n.number
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    with open(f"{base}.meta.json", "w", encoding="utf-8") as f:
        json.dump({"venue": venue_id, "invitation": inv, "api": BASE,
                   "fetched_at": stamp.isoformat(), "n_submissions": len(notes),
                   "details": None}, f, indent=2)
    print(name, len(notes), "->", base)


if __name__ == "__main__":
    fetch_pool(sys.argv[1])