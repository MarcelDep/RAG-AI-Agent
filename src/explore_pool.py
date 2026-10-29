import json
import sys
from collections import Counter

from topic import matches

pool = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8")]
vid = lambda p: p["content"].get("venueid", {}).get("value")
print("pula:", len(pool))
print("primary_area:", Counter(p["content"].get("primary_area", {}).get("value")
                               for p in pool).most_common(15))
print("statusy:", Counter(vid(p) for p in pool))
hit = [p for p in pool if matches(p)]
print("pasuje do reguły:", len(hit), Counter(vid(p) for p in hit))