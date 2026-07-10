import sys, os, json, importlib.util

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
    print("READDOCS_10 OK")

if __name__ == "__main__":
    main()
