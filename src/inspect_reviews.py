import json
import sys
from collections import Counter, defaultdict
from statistics import median

SCORE_KEYS = ("rating", "soundness", "presentation", "contribution", "confidence")
TEXT_KEYS = ("summary", "strengths", "weaknesses", "questions", "limitations")

by_status = defaultdict(lambda: [0, 0])
per_paper = Counter()
vals = defaultdict(Counter)
lens = defaultdict(list)
keys_by_type = defaultdict(set)
example = None


def val(c, k):
    v = c.get(k)
    return v.get("value") if isinstance(v, dict) else v


with open(sys.argv[1], encoding="utf-8") as f:
    for line in f:
        s = json.loads(line)
        st = s["content"].get("venueid", {}).get("value")
        reviews = []
        for r in s.get("details", {}).get("replies", []):
            t = r["invitations"][0].split("/-/")[-1]
            keys_by_type[t] |= set(r["content"])
            if t == "Official_Review":
                reviews.append(r)
        by_status[st][0] += 1
        by_status[st][1] += bool(reviews)
        per_paper[len(reviews)] += 1
        for r in reviews:
            c = r["content"]
            for k in SCORE_KEYS:
                vals[k][str(val(c, k))[:60]] += 1
            for k in TEXT_KEYS:
                v = val(c, k)
                if isinstance(v, str):
                    lens[k].append(len(v))
            if example is None:
                example = {k: str(val(c, k))[:150] for k in c}

print("\n== status: prace / z recenzją")
for st, (n, nr) in by_status.items():
    print(f"{st}: {n} / {nr}")
print("\n== liczba recenzji na pracę:", dict(sorted(per_paper.items())))
print("\n== wartości ocen")
for k in SCORE_KEYS:
    print(k, vals[k].most_common(12))
print("\n== długość pól tekstowych (znaki): mediana / max")
for k in TEXT_KEYS:
    if lens[k]:
        print(k, int(median(lens[k])), max(lens[k]), f"(n={len(lens[k])})")
print("\n== klucze content wg typu odpowiedzi")
for t, ks in keys_by_type.items():
    print(t, sorted(ks))
print("\n== przykładowa recenzja (skrócona)")
print(json.dumps(example, indent=2, ensure_ascii=False))