import sys
src, dst = sys.argv[1], sys.argv[2]
data = json.load(open(src))
t = {}
for r in data:
    t[r["user"]] = round(t.get(r["user"], 0) + r["amount"], 2)
json.dump(t, open(dst, "w"), sort_keys=True)
