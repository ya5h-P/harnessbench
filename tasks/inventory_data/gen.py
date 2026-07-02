import sys, os, json, random

workdir, gradedir, seed = sys.argv[1], sys.argv[2], int(sys.argv[3])
random.seed(seed)
cats = ["widgets", "gadgets", "sprockets", "cogs", "doohickeys"]
rows = []
lines = ["# inventory dump v3  (sku,category,qty,unit_price)"]
for i in range(400):
    sku = "SKU%04d" % i
    cat = random.choice(cats)
    qty = random.randint(1, 60)
    price = round(random.uniform(0.5, 99.5), 2)
    rows.append((sku, cat, qty, price))
    lines.append("%s,%s,%d,%.2f" % (sku, cat, qty, price))
with open(os.path.join(workdir, "inventory.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

widgets = [r for r in rows if r[1] == "widgets"]
total = round(sum(q * p for _, _, q, p in widgets), 2)
top = max(widgets, key=lambda r: r[2] * r[3])
json.dump({"total": total, "sku": top[0]},
          open(os.path.join(gradedir, "expected.json"), "w", encoding="utf-8"))
