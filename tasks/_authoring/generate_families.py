#!/usr/bin/env python3
"""Generate the templated task families (98 tasks, easy -> very hard).

These families stress the HARNESS (search, navigation, edit fidelity, tool execution,
sustained coverage), keeping per-step model difficulty low. Each family is a statistical
cluster (see score.py CLUSTER_PREFIXES).

Run once from anywhere:  python tasks/_authoring/generate_families.py
Then verify:             bash engine/preflight.sh

Idempotent: deletes and rewrites every generated family dir. Per-task content is
deterministic (seeded by task id), so regeneration is stable.
"""
import json, os, random, shutil, sys

TASKS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAMILIES = ("needle_", "bigfile_", "multiedit_", "exactout_", "chain_", "weirdfs_",
            "manyfix_", "readdocs_", "logdig_", "testfix_", "editfid_")
TIMEOUT = {1: 480, 2: 480, 3: 600, 4: 900, 5: 1500}

FILEWORDS = ("billing reports cache tokens parser export audit metrics router alerts assets "
             "backup batch broker budget carts catalog checkout clients credits devices digest "
             "drafts events feeds filters gateway history imports invoice journal labels ledger "
             "limits mailer orders payouts plans pricing profiles queue quotas ratings receipts "
             "refunds search session shipping signals storage summary support tickets uploads "
             "vendors wallets webhook").split()
PROSE = ("the service module handles routine processing for downstream consumers . operators "
         "review these records during weekly maintenance windows . this behaviour matches the "
         "original design notes from the platform team . callers should treat the response as "
         "advisory rather than binding . the retry policy follows standard exponential backoff "
         "guidance . storage compaction runs in the background without operator input . refer "
         "to the appendix for historical context on this decision").split(" . ")

# ---------------------------------------------------------------- function pool

def F(base, sig, doc, correct, buggy, cases):
    return dict(base=base, sig=sig, doc=doc, correct=correct, buggy=buggy, cases=cases)

POOL = [
    F("clamp", "(x, lo, hi)", "Clamp x into [lo, hi]. E.g. NAME(12, 1, 10) == 10; NAME(0, 1, 10) == 1.",
      "    return max(lo, min(hi, x))",
      "    return min(lo, max(hi, x))",
      [((5, 1, 10), 5), ((0, 1, 10), 1), ((12, 1, 10), 10), ((-3, -1, 1), -1)]),
    F("last_n", "(xs, n)", "Last n items of xs (all of xs if n >= len). E.g. NAME([1,2,3,4], 2) == [3, 4].",
      "    return list(xs[-n:]) if n > 0 else []",
      "    return list(xs[:n]) if n > 0 else []",
      [(([1, 2, 3, 4], 2), [3, 4]), (([1, 2], 5), [1, 2]), (([7], 1), [7])]),
    F("count_vowels", "(s)", "Number of vowels in s, case-insensitive. E.g. NAME('AeIx') == 3.",
      "    return sum(1 for ch in s.lower() if ch in \"aeiou\")",
      "    return sum(1 for ch in s if ch in \"aeiou\")",
      [(("AeIx",), 3), (("xyz",), 0), (("Onomatopoeia",), 8)]),
    F("safe_get", "(d, key, default)", "d[key] if present else default; a stored falsy value is returned as-is. E.g. NAME({'a': 0}, 'a', 9) == 0.",
      "    return d.get(key, default)",
      "    return d.get(key) or default",
      [(({"a": 0}, "a", 9), 0), (({"a": 5}, "b", 7), 7), (({}, "x", None), None)]),
    F("between", "(x, lo, hi)", "True iff lo <= x <= hi (inclusive). E.g. NAME(1, 1, 3) is True.",
      "    return lo <= x <= hi",
      "    return lo < x < hi",
      [((1, 1, 3), True), ((3, 1, 3), True), ((2, 1, 3), True), ((4, 1, 3), False)]),
    F("dedupe", "(xs)", "Remove duplicates, preserving first-seen order. E.g. NAME([3,1,3,2]) == [3, 1, 2].",
      "    seen = []\n    for x in xs:\n        if x not in seen:\n            seen.append(x)\n    return seen",
      "    return sorted(set(xs))",
      [(([3, 1, 3, 2],), [3, 1, 2]), (([1, 1, 1],), [1]), (([],), [])]),
    F("mean2", "(xs)", "Arithmetic mean rounded to 2 decimals. E.g. NAME([2, 4]) == 3.0.",
      "    return round(sum(xs) / len(xs), 2)",
      "    return round(sum(xs) / (len(xs) - 1), 2)",
      [(([2, 4],), 3.0), (([1, 2, 3],), 2.0), (([5, 5, 5, 7],), 5.5)]),
    F("c2f", "(c)", "Celsius to Fahrenheit. E.g. NAME(0) == 32.0; NAME(100) == 212.0.",
      "    return c * 9 / 5 + 32",
      "    return (c + 32) * 9 / 5",
      [((0,), 32.0), ((100,), 212.0), ((-40,), -40.0)]),
    F("initials", "(name)", "Uppercase initials of each word. E.g. NAME('ada lovelace') == 'AL'.",
      "    return \"\".join(w[0].upper() for w in name.split())",
      "    return \"\".join(w[0] for w in name.split())",
      [(("ada lovelace",), "AL"), (("grace",), "G"), (("alan m turing",), "AMT")]),
    F("running_sum", "(xs)", "Cumulative sums. E.g. NAME([1, 2, 3]) == [1, 3, 6].",
      "    total = 0\n    out = []\n    for x in xs:\n        total += x\n        out.append(total)\n    return out",
      "    total = 1\n    out = []\n    for x in xs:\n        total += x\n        out.append(total)\n    return out",
      [(([1, 2, 3],), [1, 3, 6]), (([],), []), (([5, -5],), [5, 0])]),
    F("is_pal", "(s)", "True iff s is a palindrome ignoring case and non-alphanumerics. E.g. NAME('Aba') is True.",
      "    t = [c.lower() for c in s if c.isalnum()]\n    return t == t[::-1]",
      "    t = [c for c in s if c.isalnum()]\n    return t == t[::-1]",
      [(("Aba",), True), (("No lemon, no melon",), True), (("abc",), False)]),
    F("word_count", "(s)", "Number of whitespace-separated words. E.g. NAME('a  b') == 2.",
      "    return len(s.split())",
      "    return len(s.split(\" \"))",
      [(("a  b",), 2), (("one two three",), 3), (("solo",), 1)]),
    F("pct", "(part, whole)", "part as a percentage of whole, rounded to 1 decimal. E.g. NAME(1, 8) == 12.5.",
      "    return round(100.0 * part / whole, 1)",
      "    return round(part / whole, 1)",
      [((1, 8), 12.5), ((1, 4), 25.0), ((3, 3), 100.0)]),
    F("strip_ext", "(fn)", "Filename without its LAST extension only. E.g. NAME('archive.tar.gz') == 'archive.tar'.",
      "    return fn.rsplit(\".\", 1)[0] if \".\" in fn else fn",
      "    return fn.split(\".\", 1)[0]",
      [(("archive.tar.gz",), "archive.tar"), (("readme",), "readme"), (("a.b",), "a")]),
]

FILLERS = [  # correct-only filler bodies; {n}=name, {k}=int param
    "def {n}(x):\n    return x + {k}\n",
    "def {n}(x):\n    return x * {k}\n",
    "def {n}(s):\n    return s.upper()\n",
    "def {n}(s):\n    return s.strip()\n",
    "def {n}(xs):\n    return len(xs)\n",
    "def {n}(xs):\n    return sorted(xs)\n",
    "def {n}(a, b):\n    return a if a > b else b\n",
    "def {n}(s):\n    return s[::-1]\n",
    "def {n}(x):\n    return abs(x - {k})\n",
    "def {n}(x):\n    return x % {k} == 0\n",
]

def fn_src(name, entry, body_key, indent="    "):
    doc = entry["doc"].replace("NAME", name)
    body = entry[body_key].replace("    ", indent) if indent != "    " else entry[body_key]
    return "def %s%s:\n%s\"\"\"%s\"\"\"\n%s\n" % (name, entry["sig"], indent, doc, body)

def self_check():
    for e in POOL:
        for key, want_ok in (("correct", True), ("buggy", False)):
            ns = {}
            exec(fn_src("f", e, key), ns)
            ok = all(_safe_eq(ns["f"], a, exp) for a, exp in e["cases"])
            assert ok == want_ok, "pool self-check failed: %s/%s" % (e["base"], key)

def _safe_eq(f, args, exp):
    try:
        return f(*args) == exp
    except Exception:
        return False

# ---------------------------------------------------------------- emit helpers

def emit(tid, domain, diff, prompt, files, reseed=False, notes=""):
    """files: relpath -> str (utf-8) | bytes | ('crlf', str)."""
    d = os.path.join(TASKS, tid)
    shutil.rmtree(d, ignore_errors=True)
    meta = {"id": tid, "domain": domain, "difficulty": diff, "timeout_s": TIMEOUT[diff],
            "reseed": reseed, "grader_token": tid.upper() + " OK",
            "notes": notes or "generated family task (see tasks/_authoring)"}
    files = dict(files)
    files["task.json"] = json.dumps(meta, indent=2)
    files["prompt.txt"] = prompt.strip() + "\n"
    for rel, content in files.items():
        p = os.path.join(d, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if isinstance(content, tuple) and content[0] == "crlf":
            with open(p, "wb") as f:
                f.write(content[1].replace("\r\n", "\n").replace("\n", "\r\n").encode("utf-8"))
        elif isinstance(content, bytes):
            with open(p, "wb") as f:
                f.write(content)
        else:
            with open(p, "w", encoding="utf-8", newline="\n") as f:
                f.write(content)
    COUNTS.append((tid, diff))

def rng_for(tid):
    return random.Random("hb-fam:" + tid)

def jcases(cases):
    return [[list(a), e] for a, e in cases]

# ---------------------------------------------------------------- grader templates

GRADER_GENERIC = '''import sys, os, json, importlib.util

def load_mod(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def main():
    workdir, gradedir = sys.argv[1], sys.argv[2]
    checks = json.load(open(os.path.join(gradedir, "expected.json"), encoding="utf-8"))
    for i, c in enumerate(checks):
        rel = "/".join(c["file"])
        p = os.path.join(workdir, *c["file"])
        if not os.path.exists(p):
            print("FAIL: missing file %s" % rel); sys.exit(1)
        try:
            mod = load_mod(p, "hbmod%d" % i)
        except Exception as e:
            print("FAIL: cannot import %s: %r" % (rel, e)); sys.exit(1)
        fn = getattr(mod, c["func"], None)
        if fn is None:
            print("FAIL: %s not defined in %s" % (c["func"], rel)); sys.exit(1)
        for args, exp in c["cases"]:
            try:
                got = fn(*args)
            except Exception as e:
                print("FAIL: %s(*%r) raised %r" % (c["func"], args, e)); sys.exit(1)
            if got != exp:
                print("FAIL: %s(*%r) = %r, expected %r" % (c["func"], args, got, exp)); sys.exit(1)
    print(@TOKEN@)

if __name__ == "__main__":
    main()
'''

GRADER_MULTIEDIT = '''import sys, os, json, re, importlib

def main():
    workdir, gradedir = sys.argv[1], sys.argv[2]
    spec = json.load(open(os.path.join(gradedir, "expected.json"), encoding="utf-8"))
    old, new = spec["old"], spec["new"]
    for root, _, files in os.walk(workdir):
        for f in files:
            if f.endswith(".py"):
                src = open(os.path.join(root, f), encoding="utf-8", errors="replace").read()
                if re.search(r"\\b%s\\b" % re.escape(old), src):
                    print("FAIL: old name %s still present in %s" % (old, f)); sys.exit(1)
    sys.path.insert(0, workdir)
    lib = importlib.import_module(spec["libmod"])
    if not hasattr(lib, new):
        print("FAIL: %s.%s not defined" % (spec["libmod"], new)); sys.exit(1)
    for m in spec["mods"]:
        try:
            mod = importlib.import_module(m["mod"])
        except Exception as e:
            print("FAIL: import %s: %r" % (m["mod"], e)); sys.exit(1)
        for x, exp in m["cases"]:
            try:
                got = mod.run(x)
            except Exception as e:
                print("FAIL: %s.run(%r) raised %r" % (m["mod"], x, e)); sys.exit(1)
            if got != exp:
                print("FAIL: %s.run(%r) = %r, expected %r" % (m["mod"], x, got, exp)); sys.exit(1)
    print(@TOKEN@)

if __name__ == "__main__":
    main()
'''

GRADER_TEXTFILE = '''import sys, os

def norm(s):
    return "\\n".join(ln.rstrip() for ln in s.replace("\\r\\n", "\\n").split("\\n")).strip("\\n")

def main():
    workdir, gradedir = sys.argv[1], sys.argv[2]
    target = @TARGET@
    p = os.path.join(workdir, *target.split("/"))
    if not os.path.exists(p):
        print("FAIL: missing %s" % target); sys.exit(1)
    got = norm(open(p, encoding="utf-8", errors="replace").read())
    exp = norm(open(os.path.join(gradedir, "expected_out.txt"), encoding="utf-8").read())
    if got != exp:
        print("FAIL: %s content mismatch" % target); sys.exit(1)
    print(@TOKEN@)

if __name__ == "__main__":
    main()
'''

GRADER_JSONFILE = '''import sys, os, json

def main():
    workdir, gradedir = sys.argv[1], sys.argv[2]
    target = @TARGET@
    p = os.path.join(workdir, *target.split("/"))
    if not os.path.exists(p):
        print("FAIL: missing %s" % target); sys.exit(1)
    try:
        got = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        print("FAIL: %s is not valid JSON: %r" % (target, e)); sys.exit(1)
    exp = json.load(open(os.path.join(gradedir, "expected.json"), encoding="utf-8"))
    if got != exp:
        print("FAIL: %s does not match the expected object" % target); sys.exit(1)
    print(@TOKEN@)

if __name__ == "__main__":
    main()
'''

GRADER_CHAIN = '''import sys, os, json

def norm(s):
    return "\\n".join(ln.rstrip() for ln in s.replace("\\r\\n", "\\n").split("\\n")).strip("\\n")

def main():
    workdir, gradedir = sys.argv[1], sys.argv[2]
    spec = json.load(open(os.path.join(gradedir, "chain_spec.json"), encoding="utf-8"))
    for rel in spec["required"]:
        if not os.path.exists(os.path.join(workdir, rel)):
            print("FAIL: pipeline artifact %s missing" % rel); sys.exit(1)
    final = spec["final"]
    p = os.path.join(workdir, final)
    if final.endswith(".json"):
        try:
            got = json.load(open(p, encoding="utf-8"))
        except Exception as e:
            print("FAIL: %s invalid JSON: %r" % (final, e)); sys.exit(1)
        exp = json.load(open(os.path.join(gradedir, "expected_final.json"), encoding="utf-8"))
        if got != exp:
            print("FAIL: %s does not match expected" % final); sys.exit(1)
    else:
        got = norm(open(p, encoding="utf-8", errors="replace").read())
        exp = norm(open(os.path.join(gradedir, "expected_final.txt"), encoding="utf-8").read())
        if got != exp:
            print("FAIL: %s does not match expected" % final); sys.exit(1)
    print(@TOKEN@)

if __name__ == "__main__":
    main()
'''

GRADER_TESTFIX = '''import sys, os, shutil, subprocess, tempfile

def main():
    workdir, gradedir = sys.argv[1], sys.argv[2]
    modfile = @MODFILE@
    src = os.path.join(workdir, modfile)
    if not os.path.exists(src):
        print("FAIL: %s missing" % modfile); sys.exit(1)
    tmp = tempfile.mkdtemp(prefix="hbtf_")
    shutil.copy(src, os.path.join(tmp, modfile))
    shutil.copy(os.path.join(gradedir, "tests_hidden.py"), os.path.join(tmp, "tests_hidden.py"))
    r = subprocess.run([sys.executable, "tests_hidden.py"], cwd=tmp,
                       capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        tail = (r.stdout + r.stderr).strip().splitlines()[-1:] or ["?"]
        print("FAIL: hidden tests failed: %s" % tail[0]); sys.exit(1)
    print(@TOKEN@)

if __name__ == "__main__":
    main()
'''

GRADER_READDOCS = '''import sys, os, json, importlib.util

def main():
    workdir, gradedir = sys.argv[1], sys.argv[2]
    exp = json.load(open(os.path.join(gradedir, "expected.json"), encoding="utf-8"))
    p = os.path.join(workdir, exp["module"])
    if not os.path.exists(p):
        print("FAIL: %s missing" % exp["module"]); sys.exit(1)
    spec = importlib.util.spec_from_file_location("hbfees", p)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as e:
        print("FAIL: cannot import %s: %r" % (exp["module"], e)); sys.exit(1)
    for k, v in exp["consts"].items():
        got = getattr(mod, k, None)
        if got != v:
            print("FAIL: %s = %r, docs say %r" % (k, got, v)); sys.exit(1)
    base, rate = exp["consts"][exp["basekey"]], exp["consts"][exp["ratekey"]]
    for amt in exp["amounts"]:
        want = round(base + amt * rate / 100.0, 2)
        try:
            got = mod.total_fee(amt)
        except Exception as e:
            print("FAIL: total_fee(%r) raised %r" % (amt, e)); sys.exit(1)
        if got != want:
            print("FAIL: total_fee(%r) = %r, expected %r" % (amt, got, want)); sys.exit(1)
    print(@TOKEN@)

if __name__ == "__main__":
    main()
'''

def grader(template, token, **repl):
    out = template.replace("@TOKEN@", json.dumps(token))
    for k, v in repl.items():
        out = out.replace("@%s@" % k.upper(), json.dumps(v))
    return out

# ---------------------------------------------------------------- family: needle

def make_module(rng, pool_entries, filler_n):
    """Return (source, name_map base->unique_name)."""
    parts, names = [], {}
    used = set()
    def uniq(base):
        while True:
            n = "%s_%d" % (base, rng.randrange(100, 999))
            if n not in used:
                used.add(n); return n
    items = [("pool", e) for e in pool_entries] + [("fill", None)] * filler_n
    rng.shuffle(items)
    for kind, e in items:
        if kind == "pool":
            n = uniq(e["base"]); names[e["base"]] = n
            parts.append(fn_src(n, e, "correct"))
        else:
            t = rng.choice(FILLERS)
            parts.append(t.format(n=uniq("util"), k=rng.randrange(2, 40)))
    return "\n".join(parts), names

def apply_bug(source, uname, entry):
    good = fn_src(uname, entry, "correct")
    bad = fn_src(uname, entry, "buggy")
    assert good in source, "cannot plant bug for " + uname
    return source.replace(good, bad)

def fam_needle():
    plan = [(2, 5, 1), (2, 8, 1), (3, 20, 1), (3, 30, 1), (3, 40, 1),
            (4, 70, 1), (4, 90, 1), (4, 120, 1), (5, 160, 2), (5, 200, 2)]
    for i, (diff, nfiles, nbugs) in enumerate(plan, 1):
        tid = "needle_%02d" % i
        rng = rng_for(tid)
        words = rng.sample([a + "_" + b for a in FILEWORDS for b in FILEWORDS if a != b], nfiles)
        pool = rng.sample(POOL, min(len(POOL), 6))
        buggy_entries = pool[:nbugs]
        sentinel_entries = pool[nbugs:nbugs + 3]
        files, checks, bug_lines, ref = {}, [], [], {}
        placed = {}   # base -> (file, uname)
        remaining = list(pool)
        for w in words:
            take = []
            if remaining and rng.random() < max(0.2, len(remaining) / max(1, nfiles)):
                take = [remaining.pop(0)]
            src, names = make_module(rng, take, rng.randrange(3, 6))
            fname = "app/%s.py" % w
            for e in take:
                placed[e["base"]] = (fname, names[e["base"]])
            files[fname] = src
        for e in remaining:  # anything unplaced goes in the last file
            fname = "app/%s.py" % words[-1]
            src, names = make_module(rng, [e], 0)
            files[fname] += "\n" + src
            placed[e["base"]] = (fname, names[e["base"]])
        for e in buggy_entries:   # snapshot refs BEFORE any bug lands (two bugs may share a file)
            fname, _ = placed[e["base"]]
            ref.setdefault("ref/" + fname, files[fname])
        for e in buggy_entries:
            fname, uname = placed[e["base"]]
            files[fname] = apply_bug(files[fname], uname, e)
            a, exp = e["cases"][0]
            bug_lines.append("- `%s%s` should follow its docstring: %s  (right now %s(%s) != %r)"
                             % (uname, e["sig"], e["doc"].replace("NAME", uname), uname,
                                ", ".join(repr(x) for x in a), exp))
            checks.append({"file": fname.split("/"), "func": uname, "cases": jcases(e["cases"])})
        for e in sentinel_entries:
            fname, uname = placed[e["base"]]
            checks.append({"file": fname.split("/"), "func": uname, "cases": jcases(e["cases"])})
        fixtures = {"fixtures/" + k: v for k, v in files.items()}
        prompt = ("This project has %d source file(s) under app/. %s buried somewhere in it:\n%s\n"
                  "Find the file(s) defining the function(s) above and fix the implementation(s). "
                  "Do not modify any other function."
                  % (nfiles, "One buggy function is" if nbugs == 1 else "%d buggy functions are" % nbugs,
                     "\n".join(bug_lines)))
        emit(tid, "code-search-fix", diff, prompt,
             dict(fixtures, **ref,
                  **{"grade.py": grader(GRADER_GENERIC, tid.upper() + " OK"),
                     "hidden/expected.json": json.dumps(checks)}),
             notes="needle family: locate a described function among %d files" % nfiles)

# ---------------------------------------------------------------- family: bigfile

def fam_bigfile():
    plan = [(2, 60), (2, 90), (3, 180), (3, 240), (3, 320),
            (4, 450), (4, 550), (4, 700), (5, 900), (5, 1200)]
    for i, (diff, nfuncs) in enumerate(plan, 1):
        tid = "bigfile_%02d" % i
        rng = rng_for(tid)
        pool = rng.sample(POOL, 5)
        target, sentinels = pool[0], pool[1:4]
        parts, names, used = [], {}, set()
        def uniq(base):
            while True:
                n = "%s_%d" % (base, rng.randrange(100, 9999))
                if n not in used:
                    used.add(n); return n
        slots = sorted(rng.sample(range(nfuncs), 4))
        pool_iter = iter([target] + sentinels)
        slotset = set(slots)
        for j in range(nfuncs):
            if j in slotset:
                e = next(pool_iter)
                n = uniq(e["base"]); names[e["base"]] = n
                parts.append(fn_src(n, e, "correct"))
            else:
                t = rng.choice(FILLERS)
                parts.append(t.format(n=uniq("op"), k=rng.randrange(2, 60)))
        src = "\n".join(parts)
        tname = names[target["base"]]
        ref_src = src
        src = apply_bug(src, tname, target)
        a, exp = target["cases"][0]
        checks = [{"file": ["core.py"], "func": names[e["base"]], "cases": jcases(e["cases"])}
                  for e in [target] + sentinels]
        prompt = ("core.py in this project is large (%d functions). The function `%s%s` should: %s\n"
                  "Right now %s(%s) returns the wrong value (expected %r). Fix `%s` only — every other "
                  "function in core.py must remain exactly as it is."
                  % (nfuncs, tname, target["sig"], target["doc"].replace("NAME", tname),
                     tname, ", ".join(repr(x) for x in a), exp, tname))
        emit(tid, "large-file-edit", diff, prompt,
             {"fixtures/core.py": src, "ref/core.py": ref_src,
              "grade.py": grader(GRADER_GENERIC, tid.upper() + " OK"),
              "hidden/expected.json": json.dumps(checks)},
             notes="bigfile family: precise edit in a %d-function file" % nfuncs)

# ---------------------------------------------------------------- family: multiedit

def fam_multiedit():
    plan = [(3, 3), (3, 4), (3, 5), (4, 7), (4, 8), (4, 10), (4, 12), (5, 14), (5, 16), (5, 18)]
    renames = [("clamp_value", "restrict_range"), ("apply_bounds", "bound_to"),
               ("limit_num", "cap_between"), ("fit_range", "keep_within")]
    for i, (diff, ncallers) in enumerate(plan, 1):
        tid = "multiedit_%02d" % i
        rng = rng_for(tid)
        old, new = renames[i % len(renames)]
        libmod = rng.choice(["corelib", "shared", "common", "baselib"])
        entry = POOL[0]  # clamp
        lib_old = fn_src(old, entry, "correct")
        lib_new = fn_src(new, entry, "correct")
        files = {"fixtures/%s.py" % libmod: lib_old}
        ref = {"ref/%s.py" % libmod: lib_new}
        mods = []
        words = rng.sample(FILEWORDS, ncallers)
        clampf = lambda x, lo, hi: max(lo, min(hi, x))
        for j, w in enumerate(words):
            lo = rng.randrange(0, 20); hi = lo + rng.randrange(5, 30)
            modname = "uses_%s" % w
            if j % 2 == 0:
                body_old = "from %s import %s\n\ndef run(x):\n    return %s(x, %d, %d)\n" % (libmod, old, old, lo, hi)
                body_new = "from %s import %s\n\ndef run(x):\n    return %s(x, %d, %d)\n" % (libmod, new, new, lo, hi)
            else:
                body_old = "import %s\n\ndef run(x):\n    return %s.%s(x, %d, %d)\n" % (libmod, libmod, old, lo, hi)
                body_new = "import %s\n\ndef run(x):\n    return %s.%s(x, %d, %d)\n" % (libmod, libmod, new, lo, hi)
            files["fixtures/%s.py" % modname] = body_old
            ref["ref/%s.py" % modname] = body_new
            xs = [lo - 3, lo + 2, hi + 9]
            mods.append({"mod": modname, "cases": [[x, clampf(x, lo, hi)] for x in xs]})
        spec = {"old": old, "new": new, "libmod": libmod, "mods": mods}
        prompt = ("Rename the function `%s` (defined in %s.py) to `%s` across the whole project: "
                  "the definition and every import/call site in all %d caller modules. Behavior must "
                  "be unchanged, and NO occurrence of the old name `%s` may remain anywhere "
                  "(no alias, no comment mentions)." % (old, libmod, new, ncallers, old))
        emit(tid, "cross-file-consistency", diff, prompt,
             dict(files, **ref,
                  **{"grade.py": grader(GRADER_MULTIEDIT, tid.upper() + " OK"),
                     "hidden/expected.json": json.dumps(spec)}),
             notes="multiedit family: rename across %d call sites" % ncallers)

# ---------------------------------------------------------------- family: manyfix

def fam_manyfix():
    plan = [(3, 6), (3, 8), (3, 10), (4, 12), (4, 14), (4, 17), (4, 20), (5, 23), (5, 26), (5, 28)]
    for i, (diff, nbugs) in enumerate(plan, 1):
        tid = "manyfix_%02d" % i
        rng = rng_for(tid)
        files, ref, checks = {}, {}, []
        for j in range(nbugs):
            e = POOL[j % len(POOL)]
            uname = "%s_%d" % (e["base"], rng.randrange(100, 999))
            fname = "bugs/fix_%02d.py" % (j + 1)
            files["fixtures/" + fname] = fn_src(uname, e, "buggy")
            ref["ref/" + fname] = fn_src(uname, e, "correct")
            checks.append({"file": fname.split("/"), "func": uname, "cases": jcases(e["cases"])})
        prompt = ("Every one of the %d files in bugs/ contains exactly one function with exactly one "
                  "bug. Each function's docstring states its intended behavior with worked examples. "
                  "Fix ALL of them — the task only passes when every function in every file is correct."
                  % nbugs)
        emit(tid, "bulk-fix-coverage", diff, prompt,
             dict(files, **ref,
                  **{"grade.py": grader(GRADER_GENERIC, tid.upper() + " OK"),
                     "hidden/expected.json": json.dumps(checks)}),
             notes="manyfix family: %d independent trivial fixes, all required" % nbugs)

# ---------------------------------------------------------------- family: weirdfs

WEIRD_DIRS = ["src files", "pkg (legacy)", "modules v2.1", "uber-tools", "data & docs",
              "alpha-core", "my lib", "sub.dir", "old-stuff", "final (2)", "misc  bits", "cafe"]

def fam_weirdfs():
    plan = [(2, 2, 3), (2, 2, 4), (3, 4, 8), (3, 4, 10), (3, 5, 12),
            (4, 6, 16), (4, 7, 20), (4, 7, 24)]
    for i, (diff, depth, ndecoys) in enumerate(plan, 1):
        tid = "weirdfs_%02d" % i
        rng = rng_for(tid)
        e = rng.choice(POOL)
        uname = "%s_%d" % (e["base"], rng.randrange(100, 999))
        path_parts = ["src files"] + rng.sample(WEIRD_DIRS[1:], depth - 1) + ["utils.py"]
        target_rel = "/".join(path_parts)
        files = {"fixtures/" + target_rel: fn_src(uname, e, "buggy")}
        ref = {"ref/" + target_rel: fn_src(uname, e, "correct")}
        for j in range(ndecoys):
            dparts = ["src files"] + rng.sample(WEIRD_DIRS[1:], rng.randrange(1, depth)) + \
                     [rng.choice(["utils.py", "helpers.py", "util.py"])]
            rel = "/".join(dparts)
            if "fixtures/" + rel in files:
                continue
            src, _ = make_module(rng, [], rng.randrange(2, 4))
            files["fixtures/" + rel] = src
        a, exp = e["cases"][0]
        checks = [{"file": path_parts, "func": uname, "cases": jcases(e["cases"])}]
        prompt = ("Somewhere under the directory 'src files/' (the project layout is messy — spaces, "
                  "dots and parentheses in names, several similarly named files) exactly one file "
                  "defines the function `%s%s`. It should: %s\nRight now %s(%s) returns the wrong "
                  "value (expected %r). Find that file and fix the function in place. Do not move or "
                  "rename any file." % (uname, e["sig"], e["doc"].replace("NAME", uname), uname,
                                        ", ".join(repr(x) for x in a), exp))
        emit(tid, "filesystem-robustness", diff, prompt,
             dict(files, **ref,
                  **{"grade.py": grader(GRADER_GENERIC, tid.upper() + " OK"),
                     "hidden/expected.json": json.dumps(checks)}),
             notes="weirdfs family: hostile paths, %d decoy files" % ndecoys)

# ---------------------------------------------------------------- family: exactout

def fam_exactout():
    tok = lambda tid: tid.upper() + " OK"
    # d1 static trio
    emit("exactout_01", "instruction-format-adherence", 1,
         'Create a file named hello.txt in the project root containing exactly this single line:\n'
         'Hello, HarnessBench!',
         {"fixtures/.keep": "", "ref/hello.txt": "Hello, HarnessBench!\n",
          "grade.py": grader(GRADER_TEXTFILE, tok("exactout_01"), target="hello.txt"),
          "hidden/expected_out.txt": "Hello, HarnessBench!\n"})
    emit("exactout_02", "instruction-format-adherence", 1,
         "Create a directory out/ containing two files:\n"
         "- out/a.txt with exactly the line: alpha\n- out/b.txt with exactly the line: bravo",
         {"fixtures/.keep": "", "ref/out/a.txt": "alpha\n", "ref/out/b.txt": "bravo\n",
          "grade.py": '''import sys, os
def norm(s): return s.replace("\\r\\n", "\\n").strip()
def main():
    w = sys.argv[1]
    for rel, want in (("out/a.txt", "alpha"), ("out/b.txt", "bravo")):
        p = os.path.join(w, *rel.split("/"))
        if not os.path.exists(p): print("FAIL: missing %s" % rel); sys.exit(1)
        if norm(open(p, encoding="utf-8").read()) != want:
            print("FAIL: %s wrong content" % rel); sys.exit(1)
    print("EXACTOUT_02 OK")
main()
'''})
    meta = {"name": "hb", "version": 2, "channels": ["stable", "beta"]}
    emit("exactout_03", "instruction-format-adherence", 1,
         'Create meta.json in the project root: a JSON object with exactly these keys/values:\n'
         '  "name": "hb"  (string)\n  "version": 2  (number)\n'
         '  "channels": ["stable", "beta"]  (array of strings, in this order)',
         {"fixtures/.keep": "", "ref/meta.json": json.dumps(meta, indent=1),
          "grade.py": grader(GRADER_JSONFILE, tok("exactout_03"), target="meta.json"),
          "hidden/expected.json": json.dumps(meta)})
    # d2/d3 reseeded: numbers -> stats file with exact format
    seeded = [("exactout_04", 2, "stats.txt", "min={mn}\nmax={mx}\nmean={mean:.2f}",
               "three lines: min=<int>, max=<int>, mean=<mean to exactly 2 decimals>"),
              ("exactout_05", 2, "summary.txt", "count={n}\nsum={sm}",
               "two lines: count=<how many numbers>, sum=<their integer sum>"),
              ("exactout_06", 2, "range.txt", "span={span}\nfirst={first}\nlast={last}",
               "three lines: span=<max-min>, first=<first number in the file>, last=<last number>"),
              ("exactout_07", 3, "report.txt", None,
               'a pipe table: header line "value|squared", then one line per DISTINCT input value '
               "in ascending order, formatted <value>|<value*value>"),
              ("exactout_08", 3, "buckets.txt", None,
               'one line per bucket in ascending bucket order, formatted "<bucket>: <count>", where '
               "bucket = value // 10 * 10 (integer floor to tens) and count = how many values fall in it")]
    for tid, diff, target, fmt, desc in seeded:
        gensrc = '''import json, os, random, sys
workdir, gradedir, seed = sys.argv[1], sys.argv[2], int(sys.argv[3])
rng = random.Random(seed)
nums = [rng.randrange(1, 99) for _ in range(rng.randrange(24, 40))]
open(os.path.join(workdir, "numbers.txt"), "w").write("\\n".join(map(str, nums)) + "\\n")
TID = @TID@
if TID == "exactout_04":
    out = "min=%d\\nmax=%d\\nmean=%.2f" % (min(nums), max(nums), sum(nums) / len(nums))
elif TID == "exactout_05":
    out = "count=%d\\nsum=%d" % (len(nums), sum(nums))
elif TID == "exactout_06":
    out = "span=%d\\nfirst=%d\\nlast=%d" % (max(nums) - min(nums), nums[0], nums[-1])
elif TID == "exactout_07":
    out = "value|squared\\n" + "\\n".join("%d|%d" % (v, v * v) for v in sorted(set(nums)))
else:
    from collections import Counter
    c = Counter(v // 10 * 10 for v in nums)
    out = "\\n".join("%d: %d" % (b, c[b]) for b in sorted(c))
open(os.path.join(gradedir, "expected_out.txt"), "w").write(out + "\\n")
'''.replace("@TID@", json.dumps(tid))
        solvesrc = gensrc.replace('workdir, gradedir, seed = sys.argv[1], sys.argv[2], int(sys.argv[3])',
                                  'workdir = sys.argv[1]; gradedir = workdir') \
                         .replace('rng = random.Random(seed)\nnums = [rng.randrange(1, 99) for _ in range(rng.randrange(24, 40))]\nopen(os.path.join(workdir, "numbers.txt"), "w").write("\\n".join(map(str, nums)) + "\\n")',
                                  'nums = [int(x) for x in open(os.path.join(workdir, "numbers.txt")).read().split()]') \
                         .replace('"expected_out.txt"', json.dumps(target))
        prompt = ("numbers.txt contains one integer per line. Create %s in the project root "
                  "containing exactly %s. No extra lines, no labels beyond the format given."
                  % (target, desc))
        emit(tid, "instruction-format-adherence", diff, prompt,
             {"fixtures/.keep": "", "gen.py": gensrc, "ref/solve.py": solvesrc,
              "grade.py": grader(GRADER_TEXTFILE, tok(tid), target=target)},
             reseed=True, notes="exactout family: exact-format artifact from reseeded data")

# ---------------------------------------------------------------- family: chain

CHAIN_TOOLS = {
    "keep_ok.py": '''import json, sys
src, dst = sys.argv[1], sys.argv[2]
data = json.load(open(src))
json.dump([r for r in data if r.get("ok")], open(dst, "w"))
''',
    "totals.py": '''import json, sys
src, dst = sys.argv[1], sys.argv[2]
data = json.load(open(src))
t = {}
for r in data:
    t[r["user"]] = round(t.get(r["user"], 0) + r["amount"], 2)
json.dump(t, open(dst, "w"), sort_keys=True)
''',
    "to_csv.py": '''import json, sys
src, dst = sys.argv[1], sys.argv[2]
t = json.load(open(src))
lines = ["user,total"] + ["%s,%.2f" % (u, t[u]) for u in sorted(t)]
open(dst, "w").write("\\n".join(lines) + "\\n")
''',
    "dedupe.py": '''import json, sys
src, dst = sys.argv[1], sys.argv[2]
data = json.load(open(src))
seen, out = set(), []
for r in data:
    if r["id"] not in seen:
        seen.add(r["id"]); out.append(r)
json.dump(out, open(dst, "w"))
''',
    "summary.py": '''import json, sys
src, dst = sys.argv[1], sys.argv[2]
t = json.load(open(src))
top = sorted(t, key=lambda u: (-t[u], u))[0] if t else "-"
open(dst, "w").write("users=%d\\ntop=%s\\n" % (len(t), top))
''',
}
CHAIN_BUGGY_TOTALS = CHAIN_TOOLS["totals.py"].replace("import json, sys\n", "import sys\n")

def chain_expected(records, steps):
    data = list(records)
    if "dedupe" in steps:
        seen, out = set(), []
        for r in data:
            if r["id"] not in seen:
                seen.add(r["id"]); out.append(r)
        data = out
    data = [r for r in data if r.get("ok")]
    t = {}
    for r in data:
        t[r["user"]] = round(t.get(r["user"], 0) + r["amount"], 2)
    return t

def fam_chain():
    # (diff, steps, buggy_step?)
    plan = [(2, ["keep_ok", "totals"], False), (2, ["keep_ok", "totals"], False),
            (3, ["keep_ok", "totals", "to_csv"], False), (3, ["keep_ok", "totals", "to_csv"], False),
            (3, ["keep_ok", "totals", "to_csv"], False),
            (4, ["keep_ok", "totals", "to_csv"], True), (4, ["dedupe", "keep_ok", "totals", "to_csv"], True),
            (4, ["dedupe", "keep_ok", "totals", "to_csv"], True),
            (5, ["dedupe", "keep_ok", "totals", "to_csv", "summary"], True),
            (5, ["dedupe", "keep_ok", "totals", "to_csv", "summary"], True)]
    for i, (diff, steps, buggy) in enumerate(plan, 1):
        tid = "chain_%02d" % i
        artifacts = {"dedupe": "unique.json", "keep_ok": "kept.json", "totals": "totals.json",
                     "to_csv": "final.csv", "summary": "summary.txt"}
        inputs = {"dedupe": "data.json", "keep_ok": artifacts["dedupe"] if "dedupe" in steps else "data.json",
                  "totals": "kept.json", "to_csv": "totals.json", "summary": "totals.json"}
        final = artifacts[steps[-1]]
        cmds = ["python tools/%s.py %s %s" % (s, inputs[s], artifacts[s]) for s in steps]
        files = {"fixtures/tools/%s.py" % s: CHAIN_TOOLS[s + ".py"] for s in steps}
        if buggy:
            files["fixtures/tools/totals.py"] = CHAIN_BUGGY_TOTALS
        spec = {"required": [artifacts[s] for s in steps], "final": final, "steps": steps}
        gensrc = '''import json, os, random, sys
workdir, gradedir, seed = sys.argv[1], sys.argv[2], int(sys.argv[3])
rng = random.Random(seed)
users = rng.sample(["ana", "bo", "cy", "dee", "eli", "fay", "gus", "hana"], 6)
records = [{"id": rng.randrange(1, 40), "user": rng.choice(users),
            "amount": round(rng.uniform(1, 200), 2), "ok": rng.random() < 0.7}
           for _ in range(rng.randrange(45, 70))]
json.dump(records, open(os.path.join(workdir, "data.json"), "w"))
STEPS = @STEPS@
data = list(records)
if "dedupe" in STEPS:
    seen, out = set(), []
    for r in data:
        if r["id"] not in seen:
            seen.add(r["id"]); out.append(r)
    data = out
data = [r for r in data if r.get("ok")]
t = {}
for r in data:
    t[r["user"]] = round(t.get(r["user"], 0) + r["amount"], 2)
json.dump(@SPEC@, open(os.path.join(gradedir, "chain_spec.json"), "w"))
FINAL = @FINAL@
if FINAL.endswith(".json"):
    json.dump(t, open(os.path.join(gradedir, "expected_final.json"), "w"), sort_keys=True)
elif FINAL == "final.csv":
    lines = ["user,total"] + ["%s,%.2f" % (u, t[u]) for u in sorted(t)]
    open(os.path.join(gradedir, "expected_final.txt"), "w").write("\\n".join(lines) + "\\n")
else:
    top = sorted(t, key=lambda u: (-t[u], u))[0] if t else "-"
    open(os.path.join(gradedir, "expected_final.txt"), "w").write("users=%d\\ntop=%s\\n" % (len(t), top))
'''.replace("@STEPS@", json.dumps(steps)).replace("@SPEC@", json.dumps(spec)) \
   .replace("@FINAL@", json.dumps(final))
        solvesrc = '''import json, os, sys
workdir = sys.argv[1]
STEPS = @STEPS@
ART = @ART@
IN = @IN@
records = json.load(open(os.path.join(workdir, "data.json")))
data = list(records)
if "dedupe" in STEPS:
    seen, out = set(), []
    for r in data:
        if r["id"] not in seen:
            seen.add(r["id"]); out.append(r)
    data = out
    json.dump(data, open(os.path.join(workdir, ART["dedupe"]), "w"))
data = [r for r in data if r.get("ok")]
json.dump(data, open(os.path.join(workdir, ART["keep_ok"]), "w"))
t = {}
for r in data:
    t[r["user"]] = round(t.get(r["user"], 0) + r["amount"], 2)
json.dump(t, open(os.path.join(workdir, ART["totals"]), "w"), sort_keys=True)
if "to_csv" in STEPS:
    lines = ["user,total"] + ["%s,%.2f" % (u, t[u]) for u in sorted(t)]
    open(os.path.join(workdir, ART["to_csv"]), "w").write("\\n".join(lines) + "\\n")
if "summary" in STEPS:
    top = sorted(t, key=lambda u: (-t[u], u))[0] if t else "-"
    open(os.path.join(workdir, ART["summary"]), "w").write("users=%d\\ntop=%s\\n" % (len(t), top))
'''.replace("@STEPS@", json.dumps(steps)).replace("@ART@", json.dumps(artifacts)) \
   .replace("@IN@", json.dumps(inputs))
        bugnote = ("\nNOTE: one of the step scripts has a trivial bug that makes it crash — "
                   "diagnose and fix it before/while running the pipeline." if buggy else
                   "\n(The scripts are already correct; your job is to run them.)")
        prompt = ("data.json holds transaction records. Run this %d-step pipeline from the project "
                  "root, in order:\n%s\nAll listed output files must exist afterwards; %s is the "
                  "final deliverable.%s"
                  % (len(steps), "\n".join("  %d) %s" % (k + 1, c) for k, c in enumerate(cmds)),
                     final, bugnote))
        emit(tid, "tool-pipeline", diff, prompt,
             dict(files, **{"gen.py": gensrc, "ref/solve.py": solvesrc,
                            "grade.py": grader(GRADER_CHAIN, tid.upper() + " OK")}),
             reseed=True, notes="chain family: %d-step executed pipeline%s"
                                % (len(steps), ", one buggy step" if buggy else ""))

# ---------------------------------------------------------------- family: readdocs

def prose_par(rng, n_sent):
    return " ".join(rng.choice(PROSE).strip().capitalize() + "." for _ in range(n_sent))

def fam_readdocs():
    plan = [(2, 1, 1, False), (2, 1, 1, False), (3, 3, 2, False), (3, 3, 2, False), (3, 4, 2, False),
            (4, 5, 3, True), (4, 6, 4, True), (4, 6, 4, True)]
    labels = [("BASE_FEE", "base handling fee"), ("RATE_PCT", "percentage service rate"),
              ("MAX_ITEMS", "maximum items per order"), ("GRACE_DAYS", "grace period in days")]
    for i, (diff, ndocs, nconsts, trap) in enumerate(plan, 1):
        tid = "readdocs_%02d" % i
        rng = rng_for(tid)
        modname = rng.choice(["fees.py", "pricing.py", "charges.py"])
        consts = labels[:max(2, nconsts)][:nconsts] if nconsts >= 2 else labels[:2][:1] + labels[1:2]
        consts = labels[:2] if nconsts == 1 else labels[:nconsts]
        # BASE_FEE and RATE_PCT are always present (the formula needs them)
        skel = "\n".join("%s = None  # TODO: documented under docs/" % k for k, _ in consts)
        skel += ("\n\n\ndef total_fee(amount):\n    \"\"\"round(BASE_FEE + amount * RATE_PCT / 100.0, 2)\"\"\"\n"
                 "    raise NotImplementedError\n")
        prompt_consts = ", ".join("%s (the %s)" % (k, lbl) for k, lbl in consts)
        gensrc = '''import json, os, random, sys
workdir, gradedir, seed = sys.argv[1], sys.argv[2], int(sys.argv[3])
rng = random.Random(seed)
PROSE = @PROSE@
CONSTS = @CONSTS@
NDOCS = @NDOCS@
TRAP = @TRAP@
def par(n):
    return " ".join(rng.choice(PROSE).strip().capitalize() + "." for _ in range(n))
vals = {}
for k, lbl in CONSTS:
    if k in ("MAX_ITEMS", "GRACE_DAYS"):
        vals[k] = rng.randrange(3, 60)
    else:
        vals[k] = round(rng.uniform(0.5, 9.5), 2)
docnames = ["docs/overview.md", "docs/operations.md", "docs/billing.md", "docs/changelog.md",
            "docs/faq.md", "docs/appendix.md"][:NDOCS]
paras = {d: [par(rng.randrange(3, 6)) for _ in range(rng.randrange(8, 16))] for d in docnames}
for idx, (k, lbl) in enumerate(CONSTS):
    d = docnames[idx % len(docnames)]
    sent = "As of v2, the %s is set to %s." % (lbl, json.dumps(vals[k]))
    pos = rng.randrange(len(paras[d]))
    paras[d][pos] = paras[d][pos] + " " + sent
    if TRAP:
        d2 = docnames[(idx + 1) % len(docnames)]
        old = "Historically the %s was set to %s, superseded in v2." % (
            lbl, json.dumps(round(vals[k] * 3 + 1, 2) if isinstance(vals[k], float) else vals[k] + 7))
        paras[d2][rng.randrange(len(paras[d2]))] += " " + old
for d in docnames:
    body = "# " + d.split("/")[1].replace(".md", "").title() + "\\n\\n" + "\\n\\n".join(paras[d]) + "\\n"
    p = os.path.join(workdir, *d.split("/"))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(body)
exp = {"module": @MOD@, "consts": vals, "basekey": "BASE_FEE", "ratekey": "RATE_PCT",
       "amounts": [round(rng.uniform(5, 400), 2) for _ in range(5)]}
json.dump(exp, open(os.path.join(gradedir, "expected.json"), "w"))
'''.replace("@PROSE@", json.dumps(PROSE)).replace("@CONSTS@", json.dumps(consts)) \
   .replace("@NDOCS@", json.dumps(ndocs)).replace("@TRAP@", repr(trap)) \
   .replace("@MOD@", json.dumps(modname))
        solvesrc = '''import ast, os, re, sys
workdir = sys.argv[1]
CONSTS = @CONSTS@
MOD = @MOD@
text = ""
for root, _, files in os.walk(os.path.join(workdir, "docs")):
    for f in files:
        text += open(os.path.join(root, f), encoding="utf-8").read() + "\\n"
vals = {}
for k, lbl in CONSTS:
    m = re.search(r"As of v2, the %s is set to (\\S+)\\." % re.escape(lbl), text)
    vals[k] = ast.literal_eval(m.group(1))
src = "\\n".join("%s = %r" % (k, vals[k]) for k, _ in CONSTS)
src += ("\\n\\n\\ndef total_fee(amount):\\n"
        "    return round(BASE_FEE + amount * RATE_PCT / 100.0, 2)\\n")
open(os.path.join(workdir, MOD), "w", encoding="utf-8").write(src)
'''.replace("@CONSTS@", json.dumps(consts)).replace("@MOD@", json.dumps(modname))
        trapnote = (" Some docs also mention OLD values that were 'superseded in v2' — use only "
                    "the current (v2) values." if trap else "")
        prompt = ("%s has placeholder constants: %s. Their current values are stated in the "
                  "documentation under docs/ (phrases like 'As of v2, the <name> is set to <value>')."
                  "%s Fill in every constant and implement total_fee(amount) = "
                  "round(BASE_FEE + amount * RATE_PCT / 100.0, 2)." % (modname, prompt_consts, trapnote))
        emit(tid, "doc-grounded-implementation", diff, prompt,
             {"fixtures/" + modname: skel, "gen.py": gensrc, "ref/solve.py": solvesrc,
              "grade.py": grader(GRADER_READDOCS, tid.upper() + " OK")},
             reseed=True, notes="readdocs family: %d constants across %d docs%s"
                                % (len(consts), ndocs, ", with deprecated-value traps" if trap else ""))

# ---------------------------------------------------------------- family: logdig

def fam_logdig():
    # (diff, n_lines, question)
    plan = [(2, 3000, "errors"), (2, 4000, "code"), (2, 5000, "needle"),
            (3, 12000, "between"), (3, 15000, "code"), (3, 18000, "between"),
            (4, 30000, "multi"), (4, 40000, "multi")]
    for i, (diff, nlines, q) in enumerate(plan, 1):
        tid = "logdig_%02d" % i
        gensrc = '''import json, os, random, sys
from collections import Counter
workdir, gradedir, seed = sys.argv[1], sys.argv[2], int(sys.argv[3])
rng = random.Random(seed)
N = @N@
Q = @Q@
paths = ["/api/users", "/api/orders", "/api/search", "/api/cart", "/health", "/api/export"]
levels = ["INFO"] * 12 + ["WARN"] * 3 + ["ERROR"] * 2
codes = ["E13", "E42", "E77", "W7", "I0"]
restarts = sorted(rng.sample(range(N // 5, N - N // 5), 2))
lines = []
for j in range(N):
    if j in restarts:
        lines.append("=== RESTART ===")
        continue
    lv = rng.choice(levels)
    code = rng.choice(codes)
    msg = "timeout contacting upstream" if rng.random() < 0.04 else "handled request"
    lines.append("2026-06-%02dT%02d:%02d:%02d %s code=%s id=%d path=%s %s"
                 % (1 + j * 25 // N, j % 24, (j * 7) % 60, (j * 13) % 60, lv, code,
                    rng.randrange(1000, 1400), rng.choice(paths), msg))
p = os.path.join(workdir, "logs")
os.makedirs(p, exist_ok=True)
open(os.path.join(p, "app.log"), "w").write("\\n".join(lines) + "\\n")
def parse(ln):
    parts = ln.split()
    d = {"level": parts[1]}
    for tok in parts[2:]:
        if "=" in tok:
            k, _, v = tok.partition("=")
            d[k] = v
    return d
recs = [parse(l) for l in lines if l and not l.startswith("===")]
r1, r2 = [k for k, l in enumerate(lines) if l.startswith("===")]
mid = [parse(l) for l in lines[r1 + 1:r2] if l and not l.startswith("===")]
if Q == "errors":
    out = "errors=%d" % sum(1 for r in recs if r["level"] == "ERROR")
elif Q == "code":
    out = "count=%d" % sum(1 for r in recs if r["level"] == "WARN" and r.get("code") == "W7")
elif Q == "needle":
    out = "timeouts=%d" % sum(1 for l in lines if "timeout contacting upstream" in l)
elif Q == "between":
    out = "count=%d" % sum(1 for r in mid if r["level"] == "ERROR")
else:
    errs = [r for r in recs if r["level"] == "ERROR"]
    c = Counter(r["path"] for r in errs)
    top = sorted(c, key=lambda p: (-c[p], p))[0]
    out = "errors=%d\\ntop_path=%s\\nunique_ids=%d" % (len(errs), top,
                                                       len(set(r["id"] for r in errs)))
open(os.path.join(gradedir, "expected_out.txt"), "w").write(out + "\\n")
'''.replace("@N@", json.dumps(nlines)).replace("@Q@", json.dumps(q))
        # solve.py = same analysis, reading the log, writing answer.txt
        solvesrc = gensrc.replace(
            'workdir, gradedir, seed = sys.argv[1], sys.argv[2], int(sys.argv[3])',
            'workdir = sys.argv[1]') \
            .replace('rng = random.Random(seed)', '') \
            .split("def parse(ln):")[1]
        solvesrc = ('''import os, sys
from collections import Counter
workdir = sys.argv[1]
Q = @Q@
lines = open(os.path.join(workdir, "logs", "app.log"), encoding="utf-8").read().splitlines()
def parse(ln):''' + solvesrc).replace("@Q@", json.dumps(q)) \
            .replace('open(os.path.join(gradedir, "expected_out.txt"), "w").write(out + "\\n")',
                     'open(os.path.join(workdir, "answer.txt"), "w").write(out + "\\n")')
        qdesc = {
            "errors": 'exactly one line: "errors=<number of ERROR-level lines>"',
            "code": 'exactly one line: "count=<number of WARN-level lines whose code field is W7>"',
            "needle": 'exactly one line: "timeouts=<number of lines containing the exact text '
                      '\'timeout contacting upstream\'>"',
            "between": 'exactly one line: "count=<number of ERROR-level lines strictly between the '
                       'FIRST and SECOND \'=== RESTART ===\' marker lines>"',
            "multi": 'exactly three lines:\n  errors=<total ERROR lines>\n  top_path=<path with the '
                     'most ERROR lines; ties broken alphabetically>\n  unique_ids=<number of distinct '
                     'id values among ERROR lines>',
        }[q]
        prompt = ("logs/app.log has ~%d lines in the format:\n"
                  "  <timestamp> <LEVEL> code=<code> id=<id> path=<path> <message>\n"
                  "(plus '=== RESTART ===' marker lines). It is far too large to read directly — "
                  "compute the answer with a script or shell tools. Write answer.txt in the project "
                  "root containing %s." % (nlines, qdesc))
        emit(tid, "data-extraction-at-scale", diff, prompt,
             {"fixtures/.keep": "", "gen.py": gensrc, "ref/solve.py": solvesrc,
              "grade.py": grader(GRADER_TEXTFILE, tid.upper() + " OK", target="answer.txt")},
             reseed=True, notes="logdig family: %d-line log analysis (%s)" % (nlines, q))

# ---------------------------------------------------------------- family: testfix

def fam_testfix():
    plan = [(2, 1), (2, 1), (2, 1), (3, 2), (3, 2), (3, 2), (4, 3), (4, 3)]
    for i, (diff, nbugs) in enumerate(plan, 1):
        tid = "testfix_%02d" % i
        rng = rng_for(tid)
        modname = "textkit_%d" % i
        entries = rng.sample(POOL, nbugs + 2)
        buggy_entries, ok_entries = entries[:nbugs], entries[nbugs:]
        names, parts = {}, []
        for e in entries:
            n = "%s_%d" % (e["base"], rng.randrange(100, 999))
            names[e["base"]] = n
            parts.append(fn_src(n, e, "buggy" if e in buggy_entries else "correct"))
        modsrc = "\n".join(parts)
        refsrc = "\n".join(fn_src(names[e["base"]], e, "correct") for e in entries)
        def testsrc(cases_per, label):
            ls = ["from %s import %s" % (modname, ", ".join(names[e["base"]] for e in entries)), ""]
            for e in entries:
                for a, exp in e["cases"][:cases_per]:
                    ls.append("assert %s(%s) == %r, %r" % (
                        names[e["base"]], ", ".join(repr(x) for x in a), exp,
                        names[e["base"]] + " failed"))
            ls += ["", "print(%r)" % ("%s tests passed" % label)]
            return "\n".join(ls) + "\n"
        prompt = ("tests_visible.py currently FAILS (run it: python tests_visible.py). Fix %s.py so "
                  "the visible tests pass. Grading uses a HIDDEN superset of these tests, so fix the "
                  "functions to match their docstrings — don't just game the visible asserts, and do "
                  "not edit the test file." % modname)
        emit(tid, "debug-to-green", diff, prompt,
             {"fixtures/%s.py" % modname: modsrc,
              "fixtures/tests_visible.py": testsrc(1, "visible"),
              "ref/%s.py" % modname: refsrc,
              "hidden/tests_hidden.py": testsrc(9, "hidden").replace(modname, modname),
              "grade.py": grader(GRADER_TESTFIX, tid.upper() + " OK", modfile=modname + ".py")},
             notes="testfix family: %d planted bug(s), hidden superset tests" % nbugs)

# ---------------------------------------------------------------- family: editfid

def fam_editfid():
    tok = lambda t: t.upper() + " OK"
    # 01 (d2) Makefile: tabs must survive
    mk = ("# build config\nVERSION = 1.4.2\nCC = gcc\nCFLAGS = -O2 -Wall\n\n"
          "all: prep compile package\n\nprep:\n\tmkdir -p dist\n\techo prep $(VERSION)\n\n"
          "compile: prep\n\t$(CC) $(CFLAGS) -o dist/app main.c\n\npackage: compile\n"
          "\ttar -czf dist/app-$(VERSION).tgz dist/app\n\techo done\n")
    emit("editfid_01", "edit-fidelity", 2,
         "In build.mk, change VERSION from 1.4.2 to 2.0.0. Change nothing else — recipe lines in "
         "make files MUST stay tab-indented (a tab-to-spaces conversion breaks the build).",
         {"fixtures/build.mk": mk, "ref/build.mk": mk.replace("1.4.2", "2.0.0"),
          "grade.py": '''import sys, os
def main():
    w = sys.argv[1]
    p = os.path.join(w, "build.mk")
    if not os.path.exists(p): print("FAIL: build.mk missing"); sys.exit(1)
    txt = open(p, encoding="utf-8").read().replace("\\r\\n", "\\n")
    if "VERSION = 2.0.0" not in txt: print("FAIL: VERSION not updated"); sys.exit(1)
    if "1.4.2" in txt: print("FAIL: old version still present"); sys.exit(1)
    tabs = [l for l in txt.split("\\n") if l.startswith("\\t")]
    if len(tabs) != 5: print("FAIL: expected 5 tab-indented recipe lines, found %d" % len(tabs)); sys.exit(1)
    for t in ("all:", "prep:", "compile:", "package:"):
        if t not in txt: print("FAIL: target %s lost" % t); sys.exit(1)
    print("EDITFID_01 OK")
main()
'''})
    # 02 (d2) CRLF ini
    ini = ("[server]\nhost = 127.0.0.1\nport = 8443\n\n[client]\nretries = 3\n"
           "timeout_s = 30\nverify_tls = true\n")
    emit("editfid_02", "edit-fidelity", 2,
         "settings.ini uses Windows (CRLF) line endings, and the deployment tool requires that. "
         "Change retries from 3 to 5. Keep every line ending CRLF and change nothing else.",
         {"fixtures/settings.ini": ("crlf", ini), "ref/settings.ini": ("crlf", ini.replace("retries = 3", "retries = 5")),
          "grade.py": '''import sys, os
def main():
    w = sys.argv[1]
    p = os.path.join(w, "settings.ini")
    if not os.path.exists(p): print("FAIL: settings.ini missing"); sys.exit(1)
    raw = open(p, "rb").read()
    if b"\\n" in raw.replace(b"\\r\\n", b""): print("FAIL: bare LF found - CRLF not preserved"); sys.exit(1)
    txt = raw.decode("utf-8").replace("\\r\\n", "\\n")
    want = dict(host="127.0.0.1", port="8443", retries="5", timeout_s="30", verify_tls="true")
    for k, v in want.items():
        if ("%s = %s" % (k, v)) not in txt: print("FAIL: %s should be %s" % (k, v)); sys.exit(1)
    print("EDITFID_02 OK")
main()
'''})
    # 03 (d2) minified JSON, small
    rng = rng_for("editfid_03")
    cfg = {"app": "hb", "limits": {"max_upload_mb": 25, "max_users": 500, "rate_per_min": 120},
           "features": {"beta": False, "exports": True}, "regions": ["eu-1", "us-2"]}
    fixed = json.loads(json.dumps(cfg)); fixed["limits"]["max_upload_mb"] = 100
    emit("editfid_03", "edit-fidelity", 2,
         "cfg.json is machine-generated minified JSON (one long line). Change limits.max_upload_mb "
         "from 25 to 100. Every other value must remain identical and the file must stay valid JSON.",
         {"fixtures/cfg.json": json.dumps(cfg, separators=(",", ":")),
          "ref/cfg.json": json.dumps(fixed, separators=(",", ":")),
          "grade.py": grader(GRADER_JSONFILE, tok("editfid_03"), target="cfg.json"),
          "hidden/expected.json": json.dumps(fixed)})
    # 04 (d3) one very long python dict line
    rng = rng_for("editfid_04")
    keys = ["%s_%s" % (a, b) for a in FILEWORDS[:12] for b in ("limit", "rate", "ttl", "cap", "max")]
    th = {k: rng.randrange(10, 9000) for k in rng.sample(keys, 55)}
    tgt = sorted(th)[27]
    fixed_th = dict(th); fixed_th[tgt] = 4242
    line = "THRESHOLDS = " + repr(th)
    fixed_line = "THRESHOLDS = " + repr(fixed_th)
    emit("editfid_04", "edit-fidelity", 3,
         "thresholds.py holds a single very long line defining THRESHOLDS (55 entries). Set "
         "THRESHOLDS[%r] to 4242. All 54 other entries must keep their exact current values." % tgt,
         {"fixtures/thresholds.py": line + "\n", "ref/thresholds.py": fixed_line + "\n",
          "grade.py": '''import sys, os, json, importlib.util
def main():
    w, g = sys.argv[1], sys.argv[2]
    p = os.path.join(w, "thresholds.py")
    if not os.path.exists(p): print("FAIL: thresholds.py missing"); sys.exit(1)
    spec = importlib.util.spec_from_file_location("th", p)
    mod = importlib.util.module_from_spec(spec)
    try: spec.loader.exec_module(mod)
    except Exception as e: print("FAIL: import error %r" % e); sys.exit(1)
    exp = json.load(open(os.path.join(g, "expected.json"), encoding="utf-8"))
    if getattr(mod, "THRESHOLDS", None) != exp:
        print("FAIL: THRESHOLDS does not match expected values"); sys.exit(1)
    print("EDITFID_04 OK")
main()
''',
          "hidden/expected.json": json.dumps(fixed_th)})
    # 05 (d3) unicode-dense file
    msgs = {"greeting_en": "Hello 👋 world", "greeting_de": "Hallo Welt", "greeting_ja": "こんにちは世界",
            "farewell_en": "Bye 🎉", "farewell_ja": "さようなら", "prompt_emoji": "✨🚀✨",
            "cafe": "Ça va très bien — naïve café"}
    fixed_msgs = dict(msgs); fixed_msgs["greeting_de"] = "Servus Welt 🥨"
    emit("editfid_05", "edit-fidelity", 3,
         'messages.py contains unicode-heavy strings (emoji, CJK, accents). Change MESSAGES'
         '["greeting_de"] to exactly "Servus Welt 🥨". Every other entry must remain byte-identical.',
         {"fixtures/messages.py": "MESSAGES = " + repr(msgs) + "\n",
          "ref/messages.py": "MESSAGES = " + repr(fixed_msgs) + "\n",
          "grade.py": '''import sys, os, json, importlib.util
def main():
    w, g = sys.argv[1], sys.argv[2]
    p = os.path.join(w, "messages.py")
    if not os.path.exists(p): print("FAIL: messages.py missing"); sys.exit(1)
    spec = importlib.util.spec_from_file_location("msgs", p)
    mod = importlib.util.module_from_spec(spec)
    try: spec.loader.exec_module(mod)
    except Exception as e: print("FAIL: import error %r" % e); sys.exit(1)
    exp = json.load(open(os.path.join(g, "expected.json"), encoding="utf-8"))
    if getattr(mod, "MESSAGES", None) != exp:
        print("FAIL: MESSAGES does not match expected values"); sys.exit(1)
    print("EDITFID_05 OK")
main()
''',
          "hidden/expected.json": json.dumps(fixed_msgs, ensure_ascii=False)})
    # 06 (d3) tab-indented python module
    rng = rng_for("editfid_06")
    e = POOL[5]  # dedupe
    uname = "dedupe_688"
    others = [fn_src("op_%d" % rng.randrange(100, 999),
                     rng.choice([x for x in POOL if x is not e]), "correct", indent="\t")
              for _ in range(3)]
    tabbed_buggy = fn_src(uname, e, "buggy", indent="\t")
    tabbed_ok = fn_src(uname, e, "correct", indent="\t")
    mod = "\n".join(others[:1] + [tabbed_buggy] + others[1:])
    modref = "\n".join(others[:1] + [tabbed_ok] + others[1:])
    emit("editfid_06", "edit-fidelity", 3,
         "legacy_ops.py is TAB-indented throughout (house style; do not reindent). The function "
         "dedupe_688(xs) should remove duplicates PRESERVING first-seen order, e.g. "
         "dedupe_688([3,1,3,2]) == [3, 1, 2] — currently it returns sorted output. Fix it, keeping "
         "the whole file tab-indented (a mixed-indentation file will not even import).",
         {"fixtures/legacy_ops.py": mod, "ref/legacy_ops.py": modref,
          "grade.py": ('''import sys, os, json, importlib.util
def main():
    w, g = sys.argv[1], sys.argv[2]
    p = os.path.join(w, "legacy_ops.py")
    if not os.path.exists(p): print("FAIL: legacy_ops.py missing"); sys.exit(1)
    for ln in open(p, encoding="utf-8"):
        stripped = ln.rstrip("\\n")
        if stripped and (stripped[0] == " "):
            print("FAIL: space-indented line found - file must stay tab-indented"); sys.exit(1)
    spec = importlib.util.spec_from_file_location("lops", p)
    mod = importlib.util.module_from_spec(spec)
    try: spec.loader.exec_module(mod)
    except Exception as e: print("FAIL: import error %r" % e); sys.exit(1)
    cases = json.load(open(os.path.join(g, "expected.json"), encoding="utf-8"))
    for args, exp in cases:
        got = mod.''' + uname + '''(*args)
        if got != exp: print("FAIL: %r -> %r, expected %r" % (args, got, exp)); sys.exit(1)
    print("EDITFID_06 OK")
main()
'''),
          "hidden/expected.json": json.dumps(jcases(e["cases"]))})
    # 07 (d4) big minified JSON (~4000 chars), nested change
    rng = rng_for("editfid_07")
    services = [{"name": "%s-%s" % (w, kind), "replicas": rng.randrange(1, 5),
                 "port": rng.randrange(3000, 9000),
                 "env": {"LOG_LEVEL": rng.choice(["info", "warn"]), "REGION": rng.choice(["eu-1", "us-2"])}}
                for w, kind in zip(rng.sample(FILEWORDS, 30), ["api", "worker", "svc"] * 10)]
    services[17]["name"] = "search-api"
    deploy = {"version": 3, "services": services}
    fixed_deploy = json.loads(json.dumps(deploy))
    for s in fixed_deploy["services"]:
        if s["name"] == "search-api":
            s["replicas"] = 6
    emit("editfid_07", "edit-fidelity", 4,
         "deploy.json is one long minified line describing 30 services. Find the service named "
         '"search-api" and change its "replicas" to 6. All 29 other services (and every other field) '
         "must remain exactly as they are; the file must stay valid JSON.",
         {"fixtures/deploy.json": json.dumps(deploy, separators=(",", ":")),
          "ref/deploy.json": json.dumps(fixed_deploy, separators=(",", ":")),
          "grade.py": grader(GRADER_JSONFILE, tok("editfid_07"), target="deploy.json"),
          "hidden/expected.json": json.dumps(fixed_deploy)})
    # 08 (d4) regex-pattern dict with escapes
    pats = {"ipv4": r"^\d{1,2}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",
            "iso_date": r"^\d{4}-\d{2}-\d{2}$",
            "quoted": "\"([^\"\\\\]|\\\\.)*\"",
            "money": r"\$\d+(\.\d{2})?",
            "word_b": r"\btoken\b"}
    newpat = r"^(\d{1,3}\.){3}\d{1,3}$"
    fixed_pats = dict(pats); fixed_pats["ipv4"] = newpat
    emit("editfid_08", "edit-fidelity", 4,
         "patterns.py maps names to regex strings full of backslashes and quotes. Replace the "
         "pattern for \"ipv4\" with exactly this regex (single backslashes, as a Python raw-string "
         "pattern):\n\n    ^(\\d{1,3}\\.){3}\\d{1,3}$\n\nEvery other pattern must remain exactly "
         "byte-identical, and the module must still import.",
         {"fixtures/patterns.py": "PATTERNS = " + repr(pats) + "\n",
          "ref/patterns.py": "PATTERNS = " + repr(fixed_pats) + "\n",
          "grade.py": '''import sys, os, json, importlib.util
def main():
    w, g = sys.argv[1], sys.argv[2]
    p = os.path.join(w, "patterns.py")
    if not os.path.exists(p): print("FAIL: patterns.py missing"); sys.exit(1)
    spec = importlib.util.spec_from_file_location("pats", p)
    mod = importlib.util.module_from_spec(spec)
    try: spec.loader.exec_module(mod)
    except Exception as e: print("FAIL: import error %r" % e); sys.exit(1)
    exp = json.load(open(os.path.join(g, "expected.json"), encoding="utf-8"))
    if getattr(mod, "PATTERNS", None) != exp:
        print("FAIL: PATTERNS does not match expected values"); sys.exit(1)
    print("EDITFID_08 OK")
main()
''',
          "hidden/expected.json": json.dumps(fixed_pats)})

# ---------------------------------------------------------------- main

COUNTS = []

def main():
    self_check()
    # wipe previously generated family dirs (idempotent regeneration)
    for d in os.listdir(TASKS):
        if any(d.startswith(p) for p in FAMILIES) and os.path.isdir(os.path.join(TASKS, d)):
            shutil.rmtree(os.path.join(TASKS, d))
    fam_needle(); fam_bigfile(); fam_multiedit(); fam_manyfix(); fam_weirdfs()
    fam_exactout(); fam_chain(); fam_readdocs(); fam_logdig(); fam_testfix(); fam_editfid()
    tally = {}
    for _, d in COUNTS:
        tally[d] = tally.get(d, 0) + 1
    print("generated %d tasks; difficulty tally: %s" % (len(COUNTS), dict(sorted(tally.items()))))

if __name__ == "__main__":
    main()
