import sys, os, json, importlib.util
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
