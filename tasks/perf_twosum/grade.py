import sys, os, time, random, importlib.util

def load(workdir, module, func):
    path = os.path.join(workdir, module)
    if not os.path.exists(path):
        print("FAIL: %s missing" % module); sys.exit(1)
    spec = importlib.util.spec_from_file_location(module.replace(".py", ""), path)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as e:
        print("FAIL: import error %r" % e); sys.exit(1)
    fn = getattr(mod, func, None)
    if fn is None:
        print("FAIL: %s not defined in %s" % (func, module)); sys.exit(1)
    return fn

def speedup_or_fail(naive, fast, make_input, need, token, grow):
    """Gate on relative speedup, machine-independent. Grows the input until the naive
    baseline is slow enough to time reliably, then requires need-x speedup."""
    random.seed(1234)
    size = make_input[0]
    for _ in range(6):
        data = make_input[1](size)
        t0 = time.perf_counter(); rn = naive(clone(data)); tn = time.perf_counter() - t0
        t0 = time.perf_counter(); rf = fast(clone(data)); tf = time.perf_counter() - t0
        if rf != rn:
            print("FAIL: wrong result on large input"); sys.exit(1)
        if tn >= 0.25:
            break
        size = int(size * grow)
    su = tn / max(tf, 1e-6)
    if su < need:
        print("FAIL: not fast enough (naive %.3fs vs solution %.3fs = %.1fx, need >=%.1fx)"
              % (tn, tf, su, need)); sys.exit(1)
    print("%s (%.1fx)" % (token, su))

def clone(x):
    import copy
    return copy.deepcopy(x)

def naive(nums, target):
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return True
    return False

def main():
    workdir = sys.argv[1]
    fast = load(workdir, "twosum.py", "has_pair")
    cases = [([0, 2, 4, 6], 10), ([1, 2, 3], 6), ([], 0), ([5, 5], 10), ([5], 10), ([1, 4, 4], 8)]
    for nums, t in cases:
        if fast(list(nums), t) != naive(list(nums), t):
            print("FAIL: wrong result on %r" % (nums,)); sys.exit(1)
    random.seed(1234)
    size = 4000
    for _ in range(8):
        nums = [random.randrange(0, size * 4) for _ in range(size)]
        t = size * 8 + 1  # guaranteed miss -> naive is worst-case O(n^2)
        import time
        t0 = time.perf_counter(); rn = naive(list(nums), t); tn = time.perf_counter() - t0
        t0 = time.perf_counter(); rf = fast(list(nums), t); tf = time.perf_counter() - t0
        if rf != rn:
            print("FAIL: wrong result on large input"); sys.exit(1)
        if tn >= 0.25:
            break
        size = int(size * 1.6)
    su = tn / max(tf, 1e-6)
    if su < 6.0:
        print("FAIL: not fast enough (naive %.3fs vs solution %.3fs = %.1fx, need >=6.0x)" % (tn, tf, su)); sys.exit(1)
    print("PERF_TWOSUM OK (%.1fx)" % su)

if __name__ == "__main__":
    main()
