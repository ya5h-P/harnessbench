import sys, os, time, random, importlib.util

def load(workdir):
    path = os.path.join(workdir, "dedup.py")
    spec = importlib.util.spec_from_file_location("dedup", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.dedupe

def naive(items):
    result = []
    for x in items:
        if x not in result:
            result.append(x)
    return result

def main():
    workdir = sys.argv[1]
    if not os.path.exists(os.path.join(workdir, "dedup.py")):
        print("FAIL: dedup.py missing"); sys.exit(1)
    try:
        dedupe = load(workdir)
    except Exception as e:
        print("FAIL: import error %r" % e); sys.exit(1)

    # correctness (order-preserving, strings + ints, empties)
    random.seed(7)
    for case in [[], [1], [1, 1, 1], list("abracadabra"),
                 [random.randint(0, 30) for _ in range(200)],
                 ["x", "y", "x", "z", "y"]]:
        if dedupe(list(case)) != naive(list(case)):
            print("FAIL: wrong result on %r" % (case[:8])); sys.exit(1)

    # performance gate: same large input, same machine, require >=4x speedup
    big = [random.randint(0, 200000) for _ in range(6000)]   # mostly distinct -> naive is slow
    t0 = time.perf_counter(); r_naive = naive(big); t_naive = time.perf_counter() - t0
    t0 = time.perf_counter(); r_fast = dedupe(big); t_fast = time.perf_counter() - t0
    if r_fast != r_naive:
        print("FAIL: wrong result on large input"); sys.exit(1)
    if t_naive < 0.10:
        # baseline too fast to measure reliably; fall back to a bigger input
        big = [random.randint(0, 1000000) for _ in range(12000)]
        t0 = time.perf_counter(); naive(big); t_naive = time.perf_counter() - t0
        t0 = time.perf_counter(); dedupe(big); t_fast = time.perf_counter() - t0
    speedup = t_naive / max(t_fast, 1e-6)
    if speedup < 4.0:
        print("FAIL: not fast enough (naive %.3fs vs solution %.3fs = %.1fx, need >=4x)"
              % (t_naive, t_fast, speedup)); sys.exit(1)
    print("PERF OK (%.1fx)" % speedup)

if __name__ == "__main__":
    main()
