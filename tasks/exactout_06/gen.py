import json, os, random, sys
workdir, gradedir, seed = sys.argv[1], sys.argv[2], int(sys.argv[3])
rng = random.Random(seed)
nums = [rng.randrange(1, 99) for _ in range(rng.randrange(24, 40))]
open(os.path.join(workdir, "numbers.txt"), "w").write("\n".join(map(str, nums)) + "\n")
TID = "exactout_06"
if TID == "exactout_04":
    out = "min=%d\nmax=%d\nmean=%.2f" % (min(nums), max(nums), sum(nums) / len(nums))
elif TID == "exactout_05":
    out = "count=%d\nsum=%d" % (len(nums), sum(nums))
elif TID == "exactout_06":
    out = "span=%d\nfirst=%d\nlast=%d" % (max(nums) - min(nums), nums[0], nums[-1])
elif TID == "exactout_07":
    out = "value|squared\n" + "\n".join("%d|%d" % (v, v * v) for v in sorted(set(nums)))
elif TID == "exactout_08":
    from collections import Counter
    c = Counter(v // 10 * 10 for v in nums)
    out = "\n".join("%d: %d" % (b, c[b]) for b in sorted(c))
elif TID == "exactout_09":
    ev = sum(1 for v in nums if v % 2 == 0)
    out = "evens=%d\nodds=%d" % (ev, len(nums) - ev)
elif TID == "exactout_10":
    from collections import Counter
    c = Counter(nums)
    m = sorted(c, key=lambda v: (-c[v], v))[0]
    out = "distinct=%d\nmode=%d" % (len(c), m)
elif TID == "exactout_11":
    out = "\n".join("le_%d=%d" % (t, sum(1 for v in nums if v <= t)) for t in (20, 40, 60, 80))
else:
    s = sorted(nums)
    out = "\n".join("p%d=%d" % (q, s[max(0, -(-q * len(s) // 100) - 1)]) for q in (25, 50, 75))
open(os.path.join(gradedir, "expected_out.txt"), "w").write(out + "\n")
