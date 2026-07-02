import json, os, random, sys
workdir, gradedir, seed = sys.argv[1], sys.argv[2], int(sys.argv[3])
rng = random.Random(seed)
nums = [rng.randrange(1, 99) for _ in range(rng.randrange(24, 40))]
open(os.path.join(workdir, "numbers.txt"), "w").write("\n".join(map(str, nums)) + "\n")
TID = "exactout_07"
if TID == "exactout_04":
    out = "min=%d\nmax=%d\nmean=%.2f" % (min(nums), max(nums), sum(nums) / len(nums))
elif TID == "exactout_05":
    out = "count=%d\nsum=%d" % (len(nums), sum(nums))
elif TID == "exactout_06":
    out = "span=%d\nfirst=%d\nlast=%d" % (max(nums) - min(nums), nums[0], nums[-1])
elif TID == "exactout_07":
    out = "value|squared\n" + "\n".join("%d|%d" % (v, v * v) for v in sorted(set(nums)))
else:
    from collections import Counter
    c = Counter(v // 10 * 10 for v in nums)
    out = "\n".join("%d: %d" % (b, c[b]) for b in sorted(c))
open(os.path.join(gradedir, "expected_out.txt"), "w").write(out + "\n")
