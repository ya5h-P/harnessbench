import json, os, random, sys
workdir, gradedir, seed = sys.argv[1], sys.argv[2], int(sys.argv[3])
rng = random.Random(seed)
PROSE = ["the service module handles routine processing for downstream consumers", "operators review these records during weekly maintenance windows", "this behaviour matches the original design notes from the platform team", "callers should treat the response as advisory rather than binding", "the retry policy follows standard exponential backoff guidance", "storage compaction runs in the background without operator input", "refer to the appendix for historical context on this decision"]
CONSTS = [["BASE_FEE", "base handling fee"], ["RATE_PCT", "percentage service rate"], ["MAX_ITEMS", "maximum items per order"], ["GRACE_DAYS", "grace period in days"]]
NDOCS = 6
TRAP = True
def par(n):
    return " ".join(rng.choice(PROSE).strip().capitalize() + "." for _ in range(n))
vals = {}
for k, lbl in CONSTS:
    if k in ("MAX_ITEMS", "GRACE_DAYS", "RETENTION_DAYS"):
        vals[k] = rng.randrange(3, 60)
    else:
        vals[k] = round(rng.uniform(0.5, 9.5), 2)
docnames = ["docs/overview.md", "docs/operations.md", "docs/billing.md", "docs/changelog.md",
            "docs/faq.md", "docs/appendix.md", "docs/release-notes.md", "docs/integrations.md",
            "docs/runbook.md", "docs/glossary.md"][:NDOCS]
paras = {d: [par(rng.randrange(3, 6)) for _ in range(rng.randrange(8, 16))] for d in docnames}
for idx, (k, lbl) in enumerate(CONSTS):
    d = docnames[idx % len(docnames)]
    sent = "As of v2, the %s is set to %s." % (lbl, json.dumps(vals[k]))
    pos = rng.randrange(len(paras[d]))
    paras[d][pos] = paras[d][pos] + " " + sent
    if TRAP:
        d2 = docnames[(idx + 1) % len(docnames)]
        old = "Historically the %s was set to %s, superseded in v2." % (
            lbl, json.dumps(round(vals[k] * 3 + 1, 2) if isinstance(vals[k], float) else vals[k] + 7))
        paras[d2][rng.randrange(len(paras[d2]))] += " " + old
for d in docnames:
    body = "# " + d.split("/")[1].replace(".md", "").title() + "\n\n" + "\n\n".join(paras[d]) + "\n"
    p = os.path.join(workdir, *d.split("/"))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(body)
exp = {"module": "fees.py", "consts": vals, "basekey": "BASE_FEE", "ratekey": "RATE_PCT",
       "amounts": [round(rng.uniform(5, 400), 2) for _ in range(5)]}
json.dump(exp, open(os.path.join(gradedir, "expected.json"), "w"))
