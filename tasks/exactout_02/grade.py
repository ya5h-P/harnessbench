import sys, os
def norm(s): return s.replace("\r\n", "\n").strip()
def main():
    w = sys.argv[1]
    for rel, want in (("out/a.txt", "alpha"), ("out/b.txt", "bravo")):
        p = os.path.join(w, *rel.split("/"))
        if not os.path.exists(p): print("FAIL: missing %s" % rel); sys.exit(1)
        if norm(open(p, encoding="utf-8").read()) != want:
            print("FAIL: %s wrong content" % rel); sys.exit(1)
    print("EXACTOUT_02 OK")
main()
