import sys, os, json, importlib.util
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
