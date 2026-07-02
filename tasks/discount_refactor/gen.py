import sys, os, json, random

workdir, gradedir, seed = sys.argv[1], sys.argv[2], int(sys.argv[3])
random.seed(seed)

def ref(items):
    sub = 0.0
    for price, qty in items:
        line = price * qty
        if qty >= 10:
            line *= 0.95
        sub += line
    if sub >= 500:
        sub *= 0.92
    return round(sub, 2)

cases = [[]]                       # empty case always included
# guarantee at least one order that crosses the 500 threshold and one that doesn't
cases.append([[60.0, 10], [50.0, 10]])
for _ in range(12):
    items = [[round(random.uniform(1, 80), 2), random.randint(1, 25)]
             for _ in range(random.randint(1, 4))]
    cases.append(items)

data = [{"items": c, "exp": ref(c)} for c in cases]
json.dump(data, open(os.path.join(gradedir, "cases.json"), "w", encoding="utf-8"))
# the agent only sees fixtures/discount.py (copied separately); no fixture written to workdir here
