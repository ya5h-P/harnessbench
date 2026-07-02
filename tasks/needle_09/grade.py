import sys, os, json, importlib.util

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
    print("NEEDLE_09 OK")

if __name__ == "__main__":
    main()
