import sys, os
def norm(b): return b.replace(b"\r\n", b"\n").rstrip(b"\n")
def main():
    w, g = sys.argv[1], sys.argv[2]
    p = os.path.join(w, "access.cfg")
    if not os.path.exists(p): print("FAIL: access.cfg missing"); sys.exit(1)
    got = norm(open(p, "rb").read())
    exp = norm(open(os.path.join(g, "expected.bin"), "rb").read())
    if got != exp:
        try:
            got.decode("utf-8")
            print("FAIL: access.cfg was re-encoded (decodes as UTF-8); it must stay Latin-1"); sys.exit(1)
        except UnicodeDecodeError:
            pass
        print("FAIL: access.cfg bytes differ from expected (only retries should change)"); sys.exit(1)
    print("EDITFID_08 OK")
main()
