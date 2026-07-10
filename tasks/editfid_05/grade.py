import sys, os, json, importlib.util
def main():
    w, g = sys.argv[1], sys.argv[2]
    p = os.path.join(w, "legacy_ops.py")
    if not os.path.exists(p): print("FAIL: legacy_ops.py missing"); sys.exit(1)
    for ln in open(p, encoding="utf-8"):
        stripped = ln.rstrip("\n")
        if stripped and (stripped[0] == " "):
            print("FAIL: space-indented line found - file must stay tab-indented"); sys.exit(1)
    spec = importlib.util.spec_from_file_location("lops", p)
    mod = importlib.util.module_from_spec(spec)
    try: spec.loader.exec_module(mod)
    except Exception as e: print("FAIL: import error %r" % e); sys.exit(1)
    cases = json.load(open(os.path.join(g, "expected.json"), encoding="utf-8"))
    for args, exp in cases:
        got = mod.dedupe_688(*args)
        if got != exp: print("FAIL: %r -> %r, expected %r" % (args, got, exp)); sys.exit(1)
    print("EDITFID_05 OK")
main()
