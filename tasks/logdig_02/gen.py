import json, os, random, sys
from collections import Counter
workdir, gradedir, seed = sys.argv[1], sys.argv[2], int(sys.argv[3])
rng = random.Random(seed)
N = 4000
Q = "code"
paths = ["/api/users", "/api/orders", "/api/search", "/api/cart", "/health", "/api/export"]
levels = ["INFO"] * 12 + ["WARN"] * 3 + ["ERROR"] * 2
codes = ["E13", "E42", "E77", "W7", "I0"]
restarts = sorted(rng.sample(range(N // 5, N - N // 5), 2))
lines = []
for j in range(N):
    if j in restarts:
        lines.append("=== RESTART ===")
        continue
    lv = rng.choice(levels)
    code = rng.choice(codes)
    msg = "timeout contacting upstream" if rng.random() < 0.04 else "handled request"
    lines.append("2026-06-%02dT%02d:%02d:%02d %s code=%s id=%d path=%s %s"
                 % (1 + j * 25 // N, j % 24, (j * 7) % 60, (j * 13) % 60, lv, code,
                    rng.randrange(1000, 1400), rng.choice(paths), msg))
p = os.path.join(workdir, "logs")
os.makedirs(p, exist_ok=True)
open(os.path.join(p, "app.log"), "w").write("\n".join(lines) + "\n")
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
open(os.path.join(gradedir, "expected_out.txt"), "w").write(out + "\n")
