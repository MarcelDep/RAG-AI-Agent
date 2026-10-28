import json
import sys
from collections import Counter

types, status, review_keys = Counter(), Counter(), set()
n_papers, n_with_review = 0, 0

with open(sys.argv[1], encoding="utf-8") as f:
    for line in f:
        s = json.loads(line)
        n_papers += 1
        status[s["content"].get("venueid", {}).get("value")] += 1
        has_review = False
        for r in s.get("details", {}).get("replies", []):
            suffix = r["invitations"][0].split("/-/")[-1]
            types[suffix] += 1
            if suffix == "Official_Review":
                has_review = True
                review_keys |= set(r["content"])
        n_with_review += has_review

print("prace:", n_papers, "| z recenzją:", n_with_review)
print("statusy (venueid):", dict(status))
print("typy odpowiedzi:", dict(types))
print("pola recenzji:", sorted(review_keys))