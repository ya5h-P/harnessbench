import sys, os

def norm(s):
    return "\n".join(ln.rstrip() for ln in s.replace("\r\n", "\n").split("\n")).strip("\n")

def main():
    workdir, gradedir = sys.argv[1], sys.argv[2]
    target = "answer.txt"
    p = os.path.join(workdir, *target.split("/"))
    if not os.path.exists(p):
        print("FAIL: missing %s" % target); sys.exit(1)
    got = norm(open(p, encoding="utf-8", errors="replace").read())
    exp = norm(open(os.path.join(gradedir, "expected_out.txt"), encoding="utf-8").read())
    if got != exp:
        print("FAIL: %s content mismatch" % target); sys.exit(1)
    print("LOGDIG_04 OK")

if __name__ == "__main__":
    main()
