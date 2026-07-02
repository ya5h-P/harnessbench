import json, sys
src, dst = sys.argv[1], sys.argv[2]
data = json.load(open(src))
seen, out = set(), []
for r in data:
    if r["id"] not in seen:
        seen.add(r["id"]); out.append(r)
json.dump(out, open(dst, "w"))
