import sys, os
def main():
    w, g = sys.argv[1], sys.argv[2]
    p = os.path.join(w, "build.cfg")
    if not os.path.exists(p): print("FAIL: build.cfg missing"); sys.exit(1)
    raw = open(p, "rb").read()
    if b"\n" in raw.replace(b"\r\n", b""): print("FAIL: bare LF found - CRLF not preserved"); sys.exit(1)
    tabs = [l for l in raw.split(b"\r\n") if l.startswith(b"\t")]
    if len(tabs) != 3: print("FAIL: expected 3 tab-indented recipe lines, found %d" % len(tabs)); sys.exit(1)
    exp = open(os.path.join(g, "expected.bin"), "rb").read()
    if raw.rstrip(b"\r\n") != exp.rstrip(b"\r\n"):
        print("FAIL: build.cfg bytes differ from expected (exactly two values change)"); sys.exit(1)
    print("EDITFID_11 OK")
main()
