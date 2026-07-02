import sys, os, json, subprocess

def main():
    workdir, gradedir = sys.argv[1], sys.argv[2]
    stats = os.path.join(workdir, "stats.py")
    if not os.path.exists(stats):
        print("FAIL: stats.py missing"); sys.exit(1)
    exp = json.load(open(os.path.join(gradedir, "expected.json"), encoding="utf-8"))
    nums = os.path.join(gradedir, "nums.txt")

    def run(args):
        r = subprocess.run([sys.executable, "stats.py", nums] + args, cwd=workdir,
                           capture_output=True, text=True, timeout=60)
        return r.stdout.replace("\r", "").strip(), r.stderr.strip()

    full, err = run(["--count", "--min", "--max", "--mean"])
    want = "count=%d\nmin=%d\nmax=%d\nmean=%.4f" % (exp["count"], exp["min"], exp["max"], exp["mean"])
    if full != want:
        print("FAIL: full output %r expected %r (stderr %r)" % (full, want, err[:150])); sys.exit(1)

    only, _ = run(["--mean"])
    if only != "mean=%.4f" % exp["mean"]:
        print("FAIL: --mean-only output %r" % only); sys.exit(1)

    # flag order on CLI must not change output order
    rev, _ = run(["--mean", "--max", "--min", "--count"])
    if rev != want:
        print("FAIL: output order depends on flag order: %r" % rev); sys.exit(1)

    print("STATS OK")

if __name__ == "__main__":
    main()
