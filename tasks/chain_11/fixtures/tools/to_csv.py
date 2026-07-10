import json, sys
src, dst = sys.argv[1], sys.argv[2]
t = json.load(open(src))
lines = ["user,total"] + ["%s,%.2f" % (u, t[u]) for u in sorted(t)]
open(dst, "w").write("\n".join(lines) + "\n")
