import sys, os, json

def norm(s):
    return "\n".join(ln.rstrip() for ln in s.replace("\r\n", "\n").split("\n")).strip("\n")

def main():
    workdir, gradedir = sys.argv[1], sys.argv[2]
    spec = json.load(open(os.path.join(gradedir, "chain_spec.json"), encoding="utf-8"))
    for rel in spec["required"]:
        if not os.path.exists(os.path.join(workdir, rel)):
            print("FAIL: pipeline artifact %s missing" % rel); sys.exit(1)
    final = spec["final"]
    p = os.path.join(workdir, final)
    if final.endswith(".json"):
        try:
            got = json.load(open(p, encoding="utf-8"))
        except Exception as e:
            print("FAIL: %s invalid JSON: %r" % (final, e)); sys.exit(1)
        exp = json.load(open(os.path.join(gradedir, "expected_final.json"), encoding="utf-8"))
        if got != exp:
            print("FAIL: %s does not match expected" % final); sys.exit(1)
    else:
        got = norm(open(p, encoding="utf-8", errors="replace").read())
        exp = norm(open(os.path.join(gradedir, "expected_final.txt"), encoding="utf-8").read())
        if got != exp:
            print("FAIL: %s does not match expected" % final); sys.exit(1)
    print("CHAIN_10 OK")

if __name__ == "__main__":
    main()
