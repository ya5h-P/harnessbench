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
    total = 0
    for i in range(n):
        s = 0
        for j in range(i, n):
            s += nums[j]
            if s == target:
                total += 1
    return total


def make_input(size):
    return [[random.randrange(-2, 3) for _ in range(size)], 3]

def main():
    import copy
    workdir = sys.argv[1]
    fast = load(workdir, 'subarray.py', 'count_subarrays')
    cases = [[[1,1,1], 2], [[0,0,0], 0], [[], 0], [[3,-1,-1,3], 2]]
    for c in cases:
        a = c
        if fast(*a) != naive(*a):
            print("FAIL: wrong result on %r" % (c if not isinstance(c, (list, tuple)) else str(c)[:40],)); sys.exit(1)
    random.seed(1234)
    size = 4000
    for _ in range(8):
        a = make_input(size)
        import time
        t0 = time.perf_counter(); rn = naive(*a); tn = time.perf_counter() - t0
        a2 = copy.deepcopy(a)
        t0 = time.perf_counter(); a = a2; rf = fast(*a); tf = time.perf_counter() - t0
        if rf != rn:
            print("FAIL: wrong result on large input"); sys.exit(1)
        if tn >= 0.25:
            break
        size = int(size * 1.5)
    su = tn / max(tf, 1e-6)
    if su < 6.0:
        print("FAIL: not fast enough (naive %.3fs vs solution %.3fs = %.1fx, need >=%.1fx)" % (tn, tf, su, 6.0)); sys.exit(1)
    print("PERF_SUBARRAY_TARGET OK (%.1fx)" % su)

if __name__ == "__main__":
    main()
