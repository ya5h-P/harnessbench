import json, os, random, sys
workdir = sys.argv[1]; gradedir = workdir
nums = [int(x) for x in open(os.path.join(workdir, "numbers.txt")).read().split()]
TID = "exactout_05"
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
open(os.path.join(gradedir, "summary.txt"), "w").write(out + "\n")
