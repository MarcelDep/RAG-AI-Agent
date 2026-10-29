import json
import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from fetch_openreview import make_client
from topic import matches, EFF, LLM

SEED, N = 42, 40


def is_review(n):
    return any(i.endswith("/-/Official_Review") for i in n.invitations)


def main(name, pool_path):
    pool = [json.loads(l) for l in open(pool_path, encoding="utf-8")]
    cands = sorted((p for p in pool if matches(p)), key=lambda p: p["id"])
    random.Random(SEED).shuffle(cands)

    client = make_client()
    stamp = datetime.now(timezone.utc)
    out = Path(f"data/raw/{name}_sample_threads_{stamp:%Y%m%d}.jsonl")
    kept, no_reviews = [], []
    with open(out, "w", encoding="utf-8") as f:
        for p in cands:
            if len(kept) >= N:
                break
            notes = client.get_all_notes(forum=p["id"])
            if not any(is_review(n) for n in notes):
                no_reviews.append(p["id"])
                continue
            thread = []
            for n in notes:
                rec = n.to_json()
                rec["replyto"] = n.replyto
                thread.append(rec)
            f.write(json.dumps({"paper": p, "notes": thread}, ensure_ascii=False) + "\n")
            kept.append(p["id"])
            print(name, len(kept), p["id"])
            time.sleep(0.3)

    meta = {
        "venue": name, "pool_file": str(pool_path), "seed": SEED, "target_n": N,
        "rule": "regex EFF and regex LLM on title+abstract+keywords; sorted by id; "
                "shuffled with seed; first N with >=1 Official_Review",
        "eff_regex": EFF.pattern, "llm_regex": LLM.pattern,
        "n_candidates": len(cands), "n_kept": len(kept),
        "n_skipped_no_reviews": len(no_reviews), "kept_ids": kept,
        "skipped_ids": no_reviews, "fetched_at": stamp.isoformat(),
    }
    with open(str(out).replace(".jsonl", ".meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
    print("zapisano", out, "| pominięte bez recenzji:", len(no_reviews))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])