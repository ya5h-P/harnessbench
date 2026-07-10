import sys, os, json

def main():
    workdir, gradedir = sys.argv[1], sys.argv[2]
    target = "deploy.json"
    p = os.path.join(workdir, *target.split("/"))
    if not os.path.exists(p):
        print("FAIL: missing %s" % target); sys.exit(1)
    try:
        got = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        print("FAIL: %s is not valid JSON: %r" % (target, e)); sys.exit(1)
    exp = json.load(open(os.path.join(gradedir, "expected.json"), encoding="utf-8"))
    if got != exp:
        print("FAIL: %s does not match the expected object" % target); sys.exit(1)
    print("EDITFID_06 OK")

if __name__ == "__main__":
    main()
