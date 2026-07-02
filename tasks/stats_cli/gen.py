import sys, os, json, random

workdir, gradedir, seed = sys.argv[1], sys.argv[2], int(sys.argv[3])
random.seed(seed)
n = random.randint(6, 30)
nums = [random.randint(-50, 50) for _ in range(n)]
lines = [str(x) for x in nums]
lines.insert(random.randint(0, len(lines)), "")   # a blank line to ignore
lines.insert(0, "")
with open(os.path.join(gradedir, "nums.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
exp = {"count": len(nums), "min": min(nums), "max": max(nums),
       "mean": round(sum(nums) / len(nums), 4)}
json.dump(exp, open(os.path.join(gradedir, "expected.json"), "w", encoding="utf-8"))
