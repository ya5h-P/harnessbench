import sys, os

workdir = sys.argv[1]
rows = []
with open(os.path.join(workdir, "inventory.txt"), encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        sku, cat, qty, price = line.split(",")
        rows.append((sku, cat, int(qty), float(price)))
widgets = [r for r in rows if r[1] == "widgets"]
total = round(sum(q * p for _, _, q, p in widgets), 2)
top = max(widgets, key=lambda r: r[2] * r[3])
with open(os.path.join(workdir, "result.txt"), "w", encoding="utf-8") as f:
    f.write("total=%.2f\nsku=%s\n" % (total, top[0]))
