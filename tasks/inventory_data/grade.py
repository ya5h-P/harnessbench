import sys, os, json, re

def main():
    workdir, gradedir = sys.argv[1], sys.argv[2]
    exp = json.load(open(os.path.join(gradedir, "expected.json"), encoding="utf-8"))
    rp = os.path.join(workdir, "result.txt")
    if not os.path.exists(rp):
        print("FAIL: result.txt missing"); sys.exit(1)
    txt = open(rp, encoding="utf-8").read()
    mt = re.search(r"total\s*=\s*([0-9]+(?:\.[0-9]+)?)", txt)
    ms = re.search(r"sku\s*=\s*(SKU\d+)", txt)
    if not mt or not ms:
        print("FAIL: result.txt must have total=<num> and sku=<SKU>; got %r" % txt[:120]); sys.exit(1)
    got_total = round(float(mt.group(1)), 2)
    if abs(got_total - exp["total"]) > 0.01:
        print("FAIL: total=%s expected %s" % (got_total, exp["total"])); sys.exit(1)
    if ms.group(1) != exp["sku"]:
        print("FAIL: sku=%s expected %s" % (ms.group(1), exp["sku"])); sys.exit(1)
    print("INVENTORY OK")

if __name__ == "__main__":
    main()
