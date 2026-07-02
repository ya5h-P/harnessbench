import sys, os, subprocess

def main():
    workdir = sys.argv[1]
    f = os.path.join(workdir, "greet.py")
    if not os.path.exists(f):
        print("FAIL: greet.py missing"); sys.exit(1)
    src = open(f, encoding="utf-8").read().splitlines()
    if len(src) > 12:
        print("FAIL: file has %d lines (>12)" % len(src)); sys.exit(1)
    if src and src[0].startswith("#!"):
        print("FAIL: has a shebang line"); sys.exit(1)

    r = subprocess.run([sys.executable, "greet.py", "Alice", "Bob"], cwd=workdir,
                       capture_output=True, text=True, timeout=30)
    if r.stdout.replace("\r", "") != "Hello, Alice!\nHello, Bob!\n":
        print("FAIL: bad stdout %r (stderr %r)" % (r.stdout, r.stderr[:120])); sys.exit(1)
    if r.stderr.strip():
        print("FAIL: wrote to stderr: %r" % r.stderr.strip()[:120]); sys.exit(1)

    r2 = subprocess.run([sys.executable, "-c", "import greet; print(greet.greet('X'))"],
                        cwd=workdir, capture_output=True, text=True, timeout=30)
    if r2.stdout.replace("\r", "").strip() != "Hello, X!":
        print("FAIL: greet('X')=%r" % r2.stdout.strip()); sys.exit(1)
    print("GREET OK")

if __name__ == "__main__":
    main()
