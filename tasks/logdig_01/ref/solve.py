import os, sys
from collections import Counter
workdir = sys.argv[1]
Q = "errors"
lines = open(os.path.join(workdir, "logs", "app.log"), encoding="utf-8").read().splitlines()
def parse(ln):
    parts = ln.split()
    d = {"level": parts[1]}
    for tok in parts[2:]:
        if "=" in tok:
            k, _, v = tok.partition("=")
            d[k] = v
    return d
recs = [parse(l) for l in lines if l and not l.startswith("===")]
r1, r2 = [k for k, l in enumerate(lines) if l.startswith("===")]
mid = [parse(l) for l in lines[r1 + 1:r2] if l and not l.startswith("===")]
if Q == "errors":
    out = "errors=%d" % sum(1 for r in recs if r["level"] == "ERROR")
elif Q == "code":
    out = "count=%d" % sum(1 for r in recs if r["level"] == "WARN" and r.get("code") == "W7")
elif Q == "needle":
    out = "timeouts=%d" % sum(1 for l in lines if "timeout contacting upstream" in l)
elif Q == "between":
    out = "count=%d" % sum(1 for r in mid if r["level"] == "ERROR")
else:
    errs = [r for r in recs if r["level"] == "ERROR"]
    c = Counter(r["path"] for r in errs)
    top = sorted(c, key=lambda p: (-c[p], p))[0]
    out = "errors=%d\ntop_path=%s\nunique_ids=%d" % (len(errs), top,
                                                       len(set(r["id"] for r in errs)))
open(os.path.join(workdir, "answer.txt"), "w").write(out + "\n")
