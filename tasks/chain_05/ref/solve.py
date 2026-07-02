import json, os, sys
workdir = sys.argv[1]
STEPS = ["keep_ok", "totals", "to_csv"]
ART = {"dedupe": "unique.json", "keep_ok": "kept.json", "totals": "totals.json", "to_csv": "final.csv", "summary": "summary.txt"}
IN = {"dedupe": "data.json", "keep_ok": "data.json", "totals": "kept.json", "to_csv": "totals.json", "summary": "totals.json"}
records = json.load(open(os.path.join(workdir, "data.json")))
data = list(records)
if "dedupe" in STEPS:
    seen, out = set(), []
    for r in data:
        if r["id"] not in seen:
            seen.add(r["id"]); out.append(r)
    data = out
    json.dump(data, open(os.path.join(workdir, ART["dedupe"]), "w"))
data = [r for r in data if r.get("ok")]
json.dump(data, open(os.path.join(workdir, ART["keep_ok"]), "w"))
t = {}
for r in data:
    t[r["user"]] = round(t.get(r["user"], 0) + r["amount"], 2)
json.dump(t, open(os.path.join(workdir, ART["totals"]), "w"), sort_keys=True)
if "to_csv" in STEPS:
    lines = ["user,total"] + ["%s,%.2f" % (u, t[u]) for u in sorted(t)]
    open(os.path.join(workdir, ART["to_csv"]), "w").write("\n".join(lines) + "\n")
if "summary" in STEPS:
    top = sorted(t, key=lambda u: (-t[u], u))[0] if t else "-"
    open(os.path.join(workdir, ART["summary"]), "w").write("users=%d\ntop=%s\n" % (len(t), top))
