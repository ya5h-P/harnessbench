import json, sys
src, dst = sys.argv[1], sys.argv[2]
t = json.load(open(src))
order = sorted(t, key=lambda u: (-t[u], u))
open(dst, "w").write("\n".join("%d. %s %.2f" % (i + 1, u, t[u]) for i, u in enumerate(order)) + "\n")
