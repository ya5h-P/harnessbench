import json, sys
src, dst = sys.argv[1], sys.argv[2]
t = json.load(open(src))
top = sorted(t, key=lambda u: (-t[u], u))[0] if t else "-"
open(dst, "w").write("users=%d\ntop=%s\n" % (len(t), top))
