import sys, os
def main():
    w = sys.argv[1]
    p = os.path.join(w, "build.mk")
    if not os.path.exists(p): print("FAIL: build.mk missing"); sys.exit(1)
    txt = open(p, encoding="utf-8").read().replace("\r\n", "\n")
    if "VERSION = 2.0.0" not in txt: print("FAIL: VERSION not updated"); sys.exit(1)
    if "1.4.2" in txt: print("FAIL: old version still present"); sys.exit(1)
    tabs = [l for l in txt.split("\n") if l.startswith("\t")]
    if len(tabs) != 5: print("FAIL: expected 5 tab-indented recipe lines, found %d" % len(tabs)); sys.exit(1)
    for t in ("all:", "prep:", "compile:", "package:"):
        if t not in txt: print("FAIL: target %s lost" % t); sys.exit(1)
    print("EDITFID_01 OK")
main()
