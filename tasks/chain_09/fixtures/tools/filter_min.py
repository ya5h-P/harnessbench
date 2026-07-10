import sys
src, dst = sys.argv[1], sys.argv[2]
t = json.load(open(src))
json.dump({u: v for u, v in t.items() if v >= 50}, open(dst, "w"), sort_keys=True)
