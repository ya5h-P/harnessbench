import sys, os, json, importlib.util
def main():
    w, g = sys.argv[1], sys.argv[2]
    p = os.path.join(w, "settings_all.py")
    if not os.path.exists(p): print("FAIL: settings_all.py missing"); sys.exit(1)
    spec = importlib.util.spec_from_file_location("sall", p)
    mod = importlib.util.module_from_spec(spec)
    try: spec.loader.exec_module(mod)
    except Exception as e: print("FAIL: import error %r" % e); sys.exit(1)
    exp = json.load(open(os.path.join(g, "expected.json"), encoding="utf-8"))
    got = getattr(mod, "SETTINGS", None)
    if got != exp:
        if isinstance(got, dict):
            bad = [k for k in exp if got.get(k) != exp[k]] + [k for k in got if k not in exp]
            print("FAIL: %d entries differ from expected (e.g. %s)" % (len(bad), bad[:3])); sys.exit(1)
        print("FAIL: SETTINGS does not match expected values"); sys.exit(1)
    print("EDITFID_12 OK")
main()
