import json
import random
import sys

from topic import matches

pool = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8")]
hit = sorted((p for p in pool if matches(p)), key=lambda p: p["id"])
print("kandydaci:", len(hit))
for p in random.Random(0).sample(hit, min(20, len(hit))):
    print("-", p["content"]["title"]["value"][:100])