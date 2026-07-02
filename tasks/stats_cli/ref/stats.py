import argparse

ap = argparse.ArgumentParser()
ap.add_argument("path")
for fl in ["count", "min", "max", "mean"]:
    ap.add_argument("--" + fl, action="store_true")
a = ap.parse_args()
nums = [int(x) for x in open(a.path, encoding="utf-8") if x.strip()]
if a.count:
    print("count=%d" % len(nums))
if a.min:
    print("min=%d" % min(nums))
if a.max:
    print("max=%d" % max(nums))
if a.mean:
    print("mean=%.4f" % round(sum(nums) / len(nums), 4))
