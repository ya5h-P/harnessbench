#!/usr/bin/env python3
"""Generate the v2 hand-authored task tail: performance/concurrency, security-critical,
and refactor-under-constraints. These are the categories the family generator can't
template (each has a bespoke grader), so they live here as individual emits rather than
parameterized families — but sharing one emit()/preflight contract keeps them uniform.

Run once:  python tasks/_authoring/gen_authored.py
Verify:    bash engine/preflight.sh <id>

Idempotent: rewrites each task dir it owns (listed in OWNED). Never touches family dirs
or the real-repo/hand tasks.

Contract per task (same as families):
  fixtures/ = starting state (slow | unsafe | monolithic)   -> grader MUST fail
  ref/      = reference solution                              -> grader MUST pass
  grade.py  = hidden grader, executes the artifact
Perf graders are machine-independent: they embed the naive baseline and gate on a
RELATIVE speedup (naive_time / solution_time), never an absolute wall-clock threshold.
"""
import json, os, shutil

TASKS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

OWNED = []

def emit(tid, domain, diff, timeout, prompt, files, capability, tier="variance",
         stateful=False, reseed=False, notes=""):
    d = os.path.join(TASKS, tid)
    shutil.rmtree(d, ignore_errors=True)
    meta = {"id": tid, "domain": domain, "difficulty": diff, "timeout_s": timeout,
            "reseed": reseed, "grader_token": tid.upper() + " OK",
            "capability": capability, "tier": tier, "stateful": stateful,
            "notes": notes or "hand-authored v2 task (see tasks/_authoring/gen_authored.py)"}
    files = dict(files)
    files["task.json"] = json.dumps(meta, indent=2)
    files["prompt.txt"] = prompt.strip() + "\n"
    for rel, content in files.items():
        p = os.path.join(d, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if isinstance(content, bytes):
            open(p, "wb").write(content)
        else:
            open(p, "w", encoding="utf-8", newline="\n").write(content)
    OWNED.append((tid, diff, tier))


# ============================================================ PERF / CONCURRENCY
# Shared grader preamble: load a named function from a workdir module.
LOADER = '''import sys, os, time, random, importlib.util

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
'''

def perf_task(tid, diff, module, func, sig, doc_lines, slow_body, fast_body,
              correctness_cases, naive_src, make_input_src, need, grow, tier, cap_note):
    """Emit a perf task: slow-but-correct fixture, fast ref, speedup-gated grader.

    The grader's naive baseline is the slow fixture body itself, embedded under the name
    `naive` — so the fixture provably fails the speedup gate (0 improvement) and the ref
    provably clears it. make_input args may be a single value or a list; funcs taking
    multiple args pass a list (handled by the twosum/prefix cases via _patch/list-splat)."""
    fixture = "def %s%s:\n    \"\"\"%s\"\"\"\n%s\n" % (func, sig, doc_lines, slow_body)
    ref = "def %s%s:\n    \"\"\"%s\"\"\"\n%s\n" % (func, sig, doc_lines, fast_body)
    naive_def = "def naive%s:\n%s\n" % (sig, slow_body)
    # single-arg families call fn(x); multi-arg families pass a list and splat it. We detect
    # by whether make_input returns a list intended as *args (prefix_range/topk/graph do).
    splat = tid in ("perf_prefix_range", "perf_topk_freq", "perf_graph_reach",
                    "perf_pair_count", "perf_sliding_max", "perf_subarray_target",
                    "perf_dup_within_k")
    call = "(*a)" if splat else "(a)"
    grade = LOADER + '''
%s

def make_input(size):
%s

def main():
    import copy
    workdir = sys.argv[1]
    fast = load(workdir, %r, %r)
    cases = %s
    for c in cases:
        a = c
        if fast%s != naive%s:
            print("FAIL: wrong result on %%r" %% (c if not isinstance(c, (list, tuple)) else str(c)[:40],)); sys.exit(1)
    random.seed(1234)
    size = %d
    for _ in range(8):
        a = make_input(size)
        import time
        t0 = time.perf_counter(); rn = naive%s; tn = time.perf_counter() - t0
        a2 = copy.deepcopy(a)
        t0 = time.perf_counter(); a = a2; rf = fast%s; tf = time.perf_counter() - t0
        if rf != rn:
            print("FAIL: wrong result on large input"); sys.exit(1)
        if tn >= 0.25:
            break
        size = int(size * %r)
    su = tn / max(tf, 1e-6)
    if su < %r:
        print("FAIL: not fast enough (naive %%.3fs vs solution %%.3fs = %%.1fx, need >=%%.1fx)" %% (tn, tf, su, %r)); sys.exit(1)
    print("%s (%%.1fx)" %% su)

if __name__ == "__main__":
    main()
''' % (naive_def, make_input_src, module, func, correctness_cases, call, call,
       4000, call, call, grow, need, need, tid.upper() + " OK")
    emit(tid, "performance-optimization", diff, 540 if diff == 4 else 900,
         perf_prompt(module, func, doc_lines),
         {"fixtures/" + module: fixture, "ref/" + module: ref, "grade.py": grade},
         capability="algorithmic-efficiency", tier=tier, notes=cap_note)

def perf_prompt(module, func, doc):
    return ("%s defines %s, which is correct but too slow on large inputs. Optimize it to run in "
            "roughly linear (or otherwise near-optimal) time WITHOUT changing its behavior: identical "
            "name and signature, identical results for all inputs. The grader checks correctness and "
            "then requires a substantial speedup over the current implementation on a large input. "
            "Verify by running python." % (module, func))


def perf_tasks():
    # ---- d4 (9) ----
    perf_task("perf_twosum", 4, "twosum.py", "has_pair", "(nums, target)",
              "True iff two DISTINCT indices i!=j have nums[i]+nums[j]==target.",
              "    n = len(nums)\n    for i in range(n):\n        for j in range(i + 1, n):\n"
              "            if nums[i] + nums[j] == target:\n                return True\n    return False",
              "    seen = set()\n    for x in nums:\n        if target - x in seen:\n            return True\n        seen.add(x)\n    return False",
              "[[list(range(0, 400, 2)), 799], [[1, 2, 3], 6], [[], 0], [[5, 5], 10], [[5], 10]]",
              None, "    return [random.randrange(0, size * 4) for _ in range(size)]",
              6.0, 1.6, "variance", "twosum: O(n^2) pair scan -> hashset")
    _patch_perf_naive("perf_twosum", "has_pair", "", two_arg=True)

    perf_task("perf_prefix_range", 4, "prefixrange.py", "range_sums", "(nums, queries)",
              "For each (lo, hi) in queries (inclusive indices), the sum nums[lo..hi]. Returns a list.",
              "    out = []\n    for lo, hi in queries:\n        out.append(sum(nums[lo:hi + 1]))\n    return out",
              "    pre = [0]\n    for x in nums:\n        pre.append(pre[-1] + x)\n    return [pre[hi + 1] - pre[lo] for lo, hi in queries]",
              "[[[1,2,3,4], [[0,3],[1,2],[2,2]]], [[10], [[0,0]]], [[1,1,1,1], [[0,0],[0,3]]]]",
              None,
              "    nums = [random.randrange(0, 100) for _ in range(size)]\n"
              "    qs = [tuple(sorted((random.randrange(size), random.randrange(size)))) for _ in range(size)]\n"
              "    return [nums, qs]",
              6.0, 1.5, "variance", "prefix sums: per-query O(n) slice-sum -> prefix array")

    perf_task("perf_dupfinder", 4, "dupfinder.py", "first_repeat", "(items)",
              "The first value that appears a second time (by scan order), or None if all unique.",
              "    for i in range(len(items)):\n        for j in range(i):\n            if items[i] == items[j]:\n                return items[i]\n    return None",
              "    seen = set()\n    for x in items:\n        if x in seen:\n            return x\n        seen.add(x)\n    return None",
              "[list('abcdea'), [1,2,3], [], [7,7], list('xyzzy')]",
              None, "    return [random.randrange(0, size * 3) for _ in range(size)]",
              6.0, 1.6, "variance", "dupfinder: O(n^2) -> seen-set")

    perf_task("perf_anagram", 4, "anagrams.py", "group_anagrams", "(words)",
              "Group words that are anagrams. Returns groups sorted by their sorted-letter key; "
              "within each group words keep first-seen order.",
              "    groups = []\n    keys = []\n    for w in words:\n        k = sorted(w)\n"
              "        placed = False\n        for idx in range(len(keys)):\n            if keys[idx] == k:\n"
              "                groups[idx].append(w); placed = True; break\n        if not placed:\n"
              "            keys.append(k); groups.append([w])\n    order = sorted(range(len(keys)), key=lambda i: keys[i])\n"
              "    return [groups[i] for i in order]",
              "    from collections import OrderedDict\n    d = OrderedDict()\n    for w in words:\n"
              "        d.setdefault(''.join(sorted(w)), []).append(w)\n    return [d[k] for k in sorted(d)]",
              "[['eat','tea','tan','ate','nat','bat'], [], ['a'], ['ab','ba','abc']]",
              None,
              # mostly-distinct words -> the naive keys[] list grows ~n, so its per-word linear
              # scan is genuinely O(n^2); the dict solution stays O(n).
              "    import string\n    return [''.join(random.choice(string.ascii_lowercase) for _ in range(6)) for _ in range(size)]",
              3.0, 1.7, "variance", "anagram grouping: O(n^2) key-list scan -> dict keyed by sorted letters")

    perf_task("perf_topk_freq", 4, "topk.py", "top_k", "(items, k)",
              "The k most frequent items as (item, count), most frequent first; ties broken by the "
              "item ascending. Returns a list of tuples.",
              "    uniq = []\n    for x in items:\n        if x not in uniq:\n            uniq.append(x)\n"
              "    counts = [(u, sum(1 for y in items if y == u)) for u in uniq]\n"
              "    counts.sort(key=lambda p: (-p[1], p[0]))\n    return counts[:k]",
              "    from collections import Counter\n    c = Counter(items)\n"
              "    return sorted(c.items(), key=lambda p: (-p[1], p[0]))[:k]",
              "[[list('aaabbc'), 2], [[1,1,2,3,3,3], 2], [[], 3], [[5], 1]]",
              None, "    return [[random.randrange(0, size) for _ in range(size)], 5]",
              6.0, 1.6, "variance", "top-k: O(n^2) count-by-rescan -> Counter")

    perf_task("perf_lis", 4, "lis.py", "lis_length", "(nums)",
              "Length of the longest strictly-increasing subsequence.",
              "    n = len(nums)\n    if n == 0:\n        return 0\n    best = [1] * n\n"
              "    for i in range(n):\n        for j in range(i):\n            if nums[j] < nums[i] and best[j] + 1 > best[i]:\n"
              "                best[i] = best[j] + 1\n    return max(best)",
              "    import bisect\n    tails = []\n    for x in nums:\n        i = bisect.bisect_left(tails, x)\n"
              "        if i == len(tails):\n            tails.append(x)\n        else:\n            tails[i] = x\n    return len(tails)",
              "[[3,1,2,4,1,5], [], [5,4,3], [1,2,3,4], [2,2,2]]",
              None, "    return [random.randrange(0, size) for _ in range(size)]",
              5.0, 1.5, "variance", "LIS: O(n^2) DP -> patience/bisect O(n log n)")

    perf_task("perf_graph_reach", 4, "reach.py", "reachable_count", "(n, edges, src)",
              "Number of nodes reachable from src (including src) in a directed graph with nodes "
              "0..n-1 and edges as (u, v) pairs.",
              "    reached = {src}\n    changed = True\n    while changed:\n        changed = False\n"
              "        for u, v in edges:\n            if u in reached and v not in reached:\n"
              "                reached.add(v); changed = True\n    return len(reached)",
              "    from collections import defaultdict, deque\n    g = defaultdict(list)\n"
              "    for u, v in edges:\n        g[u].append(v)\n    seen = {src}; q = deque([src])\n"
              "    while q:\n        u = q.popleft()\n        for v in g[u]:\n            if v not in seen:\n"
              "                seen.add(v); q.append(v)\n    return len(seen)",
              "[[4, [[0,1],[1,2],[3,0]], 0], [1, [], 0], [3, [[0,1],[1,2],[2,0]], 1]]",
              None,
              # a long chain with edges listed in REVERSE order: the fixpoint advances reach by
              # only one node per full pass over the edge list -> O(V*E). BFS stays O(V+E).
              "    n = size\n    edges = [[i, i + 1] for i in range(n - 1)][::-1]\n    return [n, edges, 0]",
              5.0, 1.5, "variance", "graph reach: O(V*E) fixpoint on a reverse-ordered chain -> BFS")

    perf_task("perf_pair_count", 4, "paircount.py", "count_pairs", "(nums, target)",
              "Number of index pairs i<j with nums[i]+nums[j]==target.",
              "    n = len(nums)\n    total = 0\n    for i in range(n):\n        for j in range(i + 1, n):\n"
              "            if nums[i] + nums[j] == target:\n                total += 1\n    return total",
              "    from collections import Counter\n    seen = Counter()\n    total = 0\n    for x in nums:\n"
              "        total += seen[target - x]\n        seen[x] += 1\n    return total",
              "[[[1,2,3,4], 5], [[0,0,0], 0], [[], 1], [[2,2,2,2], 4]]",
              None, "    return [[random.randrange(0, 40) for _ in range(size)], 39]",
              6.0, 1.6, "variance", "pair-count: O(n^2) -> Counter of complements")

    perf_task("perf_sliding_max", 4, "slidingmax.py", "window_maxes", "(nums, k)",
              "List of the maximum of each contiguous window of size k (len = len(nums)-k+1). "
              "Empty list if k>len(nums) or nums is empty.",
              "    if k <= 0 or k > len(nums):\n        return []\n"
              "    return [max(nums[i:i + k]) for i in range(len(nums) - k + 1)]",
              "    from collections import deque\n    if k <= 0 or k > len(nums):\n        return []\n"
              "    dq = deque(); out = []\n    for i, x in enumerate(nums):\n"
              "        while dq and nums[dq[-1]] <= x:\n            dq.pop()\n        dq.append(i)\n"
              "        if dq[0] <= i - k:\n            dq.popleft()\n        if i >= k - 1:\n            out.append(nums[dq[0]])\n    return out",
              "[[[1,3,2,5,4], 2], [[4,3,2,1], 2], [[7], 1], [[1,2], 5]]",
              None, "    return [[random.randrange(0, 1000) for _ in range(size)], 256]",
              3.0, 1.6, "variance", "sliding-window max: O(n*k) recompute -> monotonic deque O(n)")

    # ---- d5 (5) ----
    perf_task("perf_median_stream", 5, "medians.py", "running_medians", "(nums)",
              "List of running medians: element i is the median of nums[0..i]. For an even count "
              "the median is the average of the two middle values (a float).",
              "    out = []\n    seen = []\n    for x in nums:\n        seen.append(x)\n        s = sorted(seen)\n"
              "        m = len(s)\n        if m % 2:\n            out.append(float(s[m // 2]))\n        else:\n"
              "            out.append((s[m // 2 - 1] + s[m // 2]) / 2.0)\n    return out",
              "    import heapq\n    lo, hi = [], []  # lo: max-heap (neg), hi: min-heap\n    out = []\n"
              "    for x in nums:\n        if lo and x <= -lo[0]:\n            heapq.heappush(lo, -x)\n        else:\n"
              "            heapq.heappush(hi, x)\n        if len(lo) > len(hi) + 1:\n            heapq.heappush(hi, -heapq.heappop(lo))\n"
              "        elif len(hi) > len(lo):\n            heapq.heappush(lo, -heapq.heappop(hi))\n"
              "        if len(lo) == len(hi):\n            out.append((-lo[0] + hi[0]) / 2.0)\n        else:\n"
              "            out.append(float(-lo[0]))\n    return out",
              "[[1,2,3,4], [], [5], [2,1,3]]",
              None, "    return [random.randrange(0, size) for _ in range(size)]",
              6.0, 1.5, "systematic", "streaming median: O(n^2 log n) resort -> two-heap")

    perf_task("perf_subarray_target", 5, "subarray.py", "count_subarrays", "(nums, target)",
              "Number of contiguous non-empty subarrays whose sum == target.",
              "    n = len(nums)\n    total = 0\n    for i in range(n):\n        s = 0\n"
              "        for j in range(i, n):\n            s += nums[j]\n            if s == target:\n                total += 1\n    return total",
              "    from collections import Counter\n    seen = Counter({0: 1})\n    pre = 0; total = 0\n"
              "    for x in nums:\n        pre += x\n        total += seen[pre - target]\n        seen[pre] += 1\n    return total",
              "[[[1,1,1], 2], [[0,0,0], 0], [[], 0], [[3,-1,-1,3], 2]]",
              None, "    return [[random.randrange(-2, 3) for _ in range(size)], 3]",
              6.0, 1.5, "systematic", "subarray-sum count: O(n^2) -> prefix-sum Counter O(n)")

    perf_task("perf_bigram_topk", 5, "bigrams.py", "top_bigram", "(tokens)",
              "The most frequent adjacent (tokens[i], tokens[i+1]) pair as a tuple; ties broken by the "
              "pair ascending. Returns None if fewer than 2 tokens.",
              "    if len(tokens) < 2:\n        return None\n    pairs = [(tokens[i], tokens[i + 1]) for i in range(len(tokens) - 1)]\n"
              "    uniq = []\n    for p in pairs:\n        if p not in uniq:\n            uniq.append(p)\n"
              "    best = None; bc = -1\n    for p in uniq:\n        c = sum(1 for q in pairs if q == p)\n"
              "        if c > bc or (c == bc and p < best):\n            best, bc = p, c\n    return best",
              "    if len(tokens) < 2:\n        return None\n    from collections import Counter\n"
              "    c = Counter((tokens[i], tokens[i + 1]) for i in range(len(tokens) - 1))\n"
              "    return sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]",
              "PLACEHOLDER",
              None, "    return [random.choice('abcde') for _ in range(size)]",
              6.0, 1.6, "systematic", "bigram top: O(n^2) pair rescan -> Counter")
    _fix_bigram_cases("perf_bigram_topk")

    perf_task("perf_interval_stab", 5, "intervals.py", "max_overlap", "(intervals)",
              "The maximum number of intervals (given as (start, end), end exclusive) that overlap "
              "at any single point.",
              "    points = set()\n    for s, e in intervals:\n        points.add(s)\n    best = 0\n"
              "    for p in points:\n        c = sum(1 for s, e in intervals if s <= p < e)\n        if c > best:\n            best = c\n    return best",
              "    events = []\n    for s, e in intervals:\n        events.append((s, 1)); events.append((e, -1))\n"
              "    events.sort()\n    cur = best = 0\n    for _, d in events:\n        cur += d\n        if cur > best:\n            best = cur\n    return best",
              "[[(0,2),(1,3),(2,4)], [], [(0,1)], [(0,5),(1,2),(1,3),(4,6)]]",
              None,
              "    return [tuple(sorted((random.randrange(0, size), random.randrange(0, size) + 1))) for _ in range(size)]",
              5.0, 1.5, "systematic", "interval stabbing: O(n^2) point scan -> sweep line")

    perf_task("perf_dup_within_k", 5, "dupk.py", "has_dup_within", "(nums, k)",
              "True iff some value appears at two indices i<j with j-i<=k.",
              "    n = len(nums)\n    for i in range(n):\n        for j in range(i + 1, min(i + k + 1, n)):\n"
              "            if nums[i] == nums[j]:\n                return True\n    return False",
              "    window = set()\n    from collections import deque\n    order = deque()\n"
              "    for x in nums:\n        if x in window:\n            return True\n        window.add(x); order.append(x)\n"
              "        if len(order) > k:\n            window.discard(order.popleft())\n    return False",
              "[[[1,2,3,1], 3], [[1,2,3,1], 2], [[], 1], [[5,5], 1]]",
              None,
              # large k with all-distinct values -> the naive inner loop runs the full k window
              # every step (O(n*k)); the sliding-set solution is O(n).
              "    k = size // 2\n    return [list(range(size)), k]",
              5.0, 1.5, "systematic", "dup-within-k: O(n*k) window rescan -> sliding set O(n)")


def _patch_perf_naive(tid, func, naive_def, two_arg=False):
    """twosum needs a 2-arg naive + a 2-tuple make_input; rewrite its grader cleanly."""
    d = os.path.join(TASKS, tid)
    grade = LOADER + '''
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
'''
    open(os.path.join(d, "grade.py"), "w", encoding="utf-8", newline="\n").write(grade)


def _fix_bigram_cases(tid):
    """Rewrite the bigram grader's correctness cases to valid token lists."""
    p = os.path.join(TASKS, tid, "grade.py")
    src = open(p, encoding="utf-8").read()
    src = src.replace("cases = PLACEHOLDER",
                      "cases = [list('abcabcab'), list('aa'), ['x'], []]")
    open(p, "w", encoding="utf-8", newline="\n").write(src)


def main():
    perf_tasks()
    tally = {}
    for _, d, _ in OWNED:
        tally[d] = tally.get(d, 0) + 1
    print("authored %d tasks; difficulty tally: %s" % (len(OWNED), dict(sorted(tally.items()))))

if __name__ == "__main__":
    main()
