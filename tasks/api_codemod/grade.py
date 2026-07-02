import sys, os, glob, subprocess

HIDDEN = r'''
import app1, app2, app3
assert app1.run() == "alice|hi", "app1 behavior changed: %r" % (app1.run(),)
assert app2.run() == ["bob|x", "carol|y"], "app2 behavior changed: %r" % (app2.run(),)
assert app3.run() == "dave|z", "app3 behavior changed: %r" % (app3.run(),)
print("BEHAVIOR OK")
'''

def main():
    workdir = sys.argv[1]
    # completeness: no residual 'notify' anywhere
    residual = []
    for f in glob.glob(os.path.join(workdir, "**", "*.py"), recursive=True):
        try:
            if "notify" in open(f, encoding="utf-8").read():
                residual.append(os.path.basename(f))
        except Exception:
            pass
    if residual:
        print("FAIL: 'notify' still present in: %s" % ", ".join(sorted(set(residual)))); sys.exit(1)

    # behavior preserved
    r = subprocess.run([sys.executable, "-c", HIDDEN], cwd=workdir,
                       capture_output=True, text=True, timeout=60)
    if "BEHAVIOR OK" not in r.stdout or r.returncode != 0:
        msg = (r.stderr.strip().splitlines() or [r.stdout.strip() or "?"])[-1]
        print("FAIL: " + msg[:200]); sys.exit(1)
    print("CODEMOD OK")

if __name__ == "__main__":
    main()
