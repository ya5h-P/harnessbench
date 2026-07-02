import sys, os, importlib.util
def load(wd, n):
    s = importlib.util.spec_from_file_location(n, os.path.join(wd, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def main():
    wd = sys.argv[1]
    if not os.path.exists(os.path.join(wd, "strutils.py")):
        print("FAIL: strutils.py missing"); sys.exit(1)
    try:
        m = load(wd, "strutils"); c = m.cardinalize; pluralize = m.pluralize
    except Exception as e:
        print("FAIL: import %r" % e); sys.exit(1)
    # Truth = the module's OWN pluralize, so we test cardinalize's count LOGIC (what the bug breaks),
    # independent of how (im)perfect boltons' pluralizer is.
    for noun in ["vowel", "box", "Wish", "cat", "dog", "church", "day"]:
        if c(noun, 1) != noun:
            print("FAIL: cardinalize(%r, 1)=%r expected %r" % (noun, c(noun, 1), noun)); sys.exit(1)
        for count in [0, 2, 3, 5]:
            exp = pluralize(noun)
            if c(noun, count) != exp:
                print("FAIL: cardinalize(%r, %r)=%r expected %r" % (noun, count, c(noun, count), exp)); sys.exit(1)
    print("CARDINAL OK")

if __name__ == "__main__":
    main()
