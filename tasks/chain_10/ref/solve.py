import json, os, sys
workdir = sys.argv[1]
STEPS = ["dedupe", "keep_ok", "totals", "filter_min", "to_csv", "rank"]
ART = {"dedupe": "unique.json", "keep_ok": "kept.json", "totals": "totals.json", "filter_min": "filtered.json", "to_csv": "final.csv", "rank": "ranking.txt", "summary": "summary.txt"}
IN = {"dedupe": "data.json", "keep_ok": "unique.json", "totals": "kept.json", "filter_min": "totals.json", "to_csv": "filtered.json", "rank": "filtered.json"}
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
basis = t
if "filter_min" in STEPS:
    basis = {u: v for u, v in t.items() if v >= 50}
    json.dump(basis, open(os.path.join(workdir, ART["filter_min"]), "w"), sort_keys=True)
if "to_csv" in STEPS:
    lines = ["user,total"] + ["%s,%.2f" % (u, basis[u]) for u in sorted(basis)]
    open(os.path.join(workdir, ART["to_csv"]), "w").write("\n".join(lines) + "\n")
if "rank" in STEPS:
    order = sorted(basis, key=lambda u: (-basis[u], u))
    open(os.path.join(workdir, ART["rank"]), "w").write(
        "\n".join("%d. %s %.2f" % (i + 1, u, basis[u]) for i, u in enumerate(order)) + "\n")
if "summary" in STEPS:
    top = sorted(basis, key=lambda u: (-basis[u], u))[0] if basis else "-"
    open(os.path.join(workdir, ART["summary"]), "w").write("users=%d\ntop=%s\n" % (len(basis), top))
