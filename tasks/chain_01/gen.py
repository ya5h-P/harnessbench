import json, os, random, sys
workdir, gradedir, seed = sys.argv[1], sys.argv[2], int(sys.argv[3])
rng = random.Random(seed)
users = rng.sample(["ana", "bo", "cy", "dee", "eli", "fay", "gus", "hana"], 6)
records = [{"id": rng.randrange(1, 40), "user": rng.choice(users),
            "amount": round(rng.uniform(1, 200), 2), "ok": rng.random() < 0.7}
           for _ in range(rng.randrange(45, 70))]
json.dump(records, open(os.path.join(workdir, "data.json"), "w"))
STEPS = ["keep_ok", "totals", "to_csv"]
data = list(records)
if "dedupe" in STEPS:
    seen, out = set(), []
    for r in data:
        if r["id"] not in seen:
            seen.add(r["id"]); out.append(r)
    data = out
data = [r for r in data if r.get("ok")]
t = {}
for r in data:
    t[r["user"]] = round(t.get(r["user"], 0) + r["amount"], 2)
basis = {u: v for u, v in t.items() if v >= 50} if "filter_min" in STEPS else t
json.dump({"required": ["kept.json", "totals.json", "final.csv"], "final": "final.csv", "steps": ["keep_ok", "totals", "to_csv"]}, open(os.path.join(gradedir, "chain_spec.json"), "w"))
FINAL = "final.csv"
if FINAL.endswith(".json"):
    json.dump(basis, open(os.path.join(gradedir, "expected_final.json"), "w"), sort_keys=True)
elif FINAL == "final.csv":
    lines = ["user,total"] + ["%s,%.2f" % (u, basis[u]) for u in sorted(basis)]
    open(os.path.join(gradedir, "expected_final.txt"), "w").write("\n".join(lines) + "\n")
elif FINAL == "ranking.txt":
    order = sorted(basis, key=lambda u: (-basis[u], u))
    open(os.path.join(gradedir, "expected_final.txt"), "w").write(
        "\n".join("%d. %s %.2f" % (i + 1, u, basis[u]) for i, u in enumerate(order)) + "\n")
else:
    top = sorted(basis, key=lambda u: (-basis[u], u))[0] if basis else "-"
    open(os.path.join(gradedir, "expected_final.txt"), "w").write("users=%d\ntop=%s\n" % (len(basis), top))
