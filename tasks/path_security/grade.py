import sys, os, subprocess

HIDDEN = r'''
import os
os.makedirs("docs", exist_ok=True)
with open(os.path.join("docs", "hello.txt"), "w", encoding="utf-8") as f:
    f.write("hi there")
with open("secret.txt", "w", encoding="utf-8") as f:
    f.write("TOPSECRET")
from fileserver import read_doc

# 1. legitimate read must still work
if read_doc("hello.txt").strip() != "hi there":
    raise SystemExit("legit read broken")

def blocked(arg):
    try:
        read_doc(arg)
        return False
    except Exception:
        return True

# 2. traversal + absolute paths must be refused (raise), not read
attacks = ["../secret.txt", "../../secret.txt", os.path.abspath("secret.txt"),
           "docs/../../secret.txt", "..%s.." % os.sep + os.sep + "secret.txt"]
for a in attacks:
    if not blocked(a):
        raise SystemExit("traversal NOT blocked: %r" % a)
print("SECURITY OK")
'''

def main():
    workdir = sys.argv[1]
    if not os.path.exists(os.path.join(workdir, "fileserver.py")):
        print("FAIL: fileserver.py missing"); sys.exit(1)
    r = subprocess.run([sys.executable, "-c", HIDDEN], cwd=workdir,
                       capture_output=True, text=True, timeout=60)
    if "SECURITY OK" in r.stdout and r.returncode == 0:
        print("SECURITY OK"); sys.exit(0)
    msg = (r.stderr.strip().splitlines() or [r.stdout.strip() or "?"])[-1]
    print("FAIL: " + msg[:200]); sys.exit(1)

if __name__ == "__main__":
    main()
