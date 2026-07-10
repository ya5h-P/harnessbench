import sys, os, json, re, importlib

def main():
    workdir, gradedir = sys.argv[1], sys.argv[2]
    spec = json.load(open(os.path.join(gradedir, "expected.json"), encoding="utf-8"))
    old, new = spec["old"], spec["new"]
    for root, _, files in os.walk(workdir):
        for f in files:
            if f.endswith(".py"):
                src = open(os.path.join(root, f), encoding="utf-8", errors="replace").read()
                if re.search(r"\b%s\b" % re.escape(old), src):
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
    print("MULTIEDIT_16 OK")

if __name__ == "__main__":
    main()
