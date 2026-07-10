import sys, os
def norm(b): return b.replace(b"\r\n", b"\n").rstrip(b"\n")
def main():
    w, g = sys.argv[1], sys.argv[2]
    p = os.path.join(w, "inventory.dat")
    if not os.path.exists(p): print("FAIL: inventory.dat missing"); sys.exit(1)
    got = norm(open(p, "rb").read())
    exp = norm(open(os.path.join(g, "expected.bin"), "rb").read())
    if got != exp:
        gl, el = got.split(b"\n"), exp.split(b"\n")
        if len(gl) != len(el):
            print("FAIL: expected %d data rows, found %d" % (len(el), len(gl))); sys.exit(1)
        for i, (a, b) in enumerate(zip(gl, el)):
            if a != b:
                print("FAIL: row %d differs (column alignment/padding must be preserved exactly)" % (i + 1)); sys.exit(1)
        print("FAIL: content differs"); sys.exit(1)
    print("EDITFID_10 OK")
main()
