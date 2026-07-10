import ast, os, re, sys
workdir = sys.argv[1]
CONSTS = [["BASE_FEE", "base handling fee"], ["RATE_PCT", "percentage service rate"], ["MAX_ITEMS", "maximum items per order"], ["GRACE_DAYS", "grace period in days"], ["SURCHARGE_PCT", "peak-hours surcharge percentage"], ["RETENTION_DAYS", "record retention period in days"]]
MOD = "fees.py"
text = ""
for root, _, files in os.walk(os.path.join(workdir, "docs")):
    for f in files:
        text += open(os.path.join(root, f), encoding="utf-8").read() + "\n"
vals = {}
for k, lbl in CONSTS:
    m = re.search(r"As of v2, the %s is set to (\S+)\." % re.escape(lbl), text)
    vals[k] = ast.literal_eval(m.group(1))
src = "\n".join("%s = %r" % (k, vals[k]) for k, _ in CONSTS)
src += ("\n\n\ndef total_fee(amount):\n"
        "    return round(BASE_FEE + amount * RATE_PCT / 100.0, 2)\n")
open(os.path.join(workdir, MOD), "w", encoding="utf-8").write(src)
