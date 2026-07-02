import sys, os, json, importlib.util

def main():
    workdir, gradedir = sys.argv[1], sys.argv[2]
    path = os.path.join(workdir, "discount.py")
    if not os.path.exists(path):
        print("FAIL: discount.py missing"); sys.exit(1)
    try:
        spec = importlib.util.spec_from_file_location("discount", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        fp = mod.final_price
    except Exception as e:
        print("FAIL: import error %r" % e); sys.exit(1)

    cases = json.load(open(os.path.join(gradedir, "cases.json"), encoding="utf-8"))
    for c in cases:
        items = [tuple(i) for i in c["items"]]
        try:
            got = fp(items)
        except Exception as e:
            print("FAIL: final_price(%r) raised %r" % (items, e)); sys.exit(1)
        if abs(got - c["exp"]) > 1e-9:
            print("FAIL: final_price(%r)=%r expected %r" % (items, got, c["exp"])); sys.exit(1)
    if fp([]) != 0.0:
        print("FAIL: empty list must return 0.0, got %r" % fp([])); sys.exit(1)
    print("DISCOUNT OK")

if __name__ == "__main__":
    main()
