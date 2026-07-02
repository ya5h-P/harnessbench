import sys, os, re, shutil, subprocess

def main():
    workdir = sys.argv[1]
    src = os.path.join(workdir, "papergen.py")
    if not os.path.exists(src):
        print("FAIL: papergen.py missing"); sys.exit(1)
    gdir = os.path.join(workdir, "_grade_papergen")
    shutil.rmtree(gdir, ignore_errors=True); os.makedirs(gdir)
    shutil.copy(src, os.path.join(gdir, "papergen.py"))
    p = subprocess.run([sys.executable, "papergen.py"], cwd=gdir,
                       capture_output=True, text=True, timeout=60)
    if p.returncode != 0:
        print("FAIL: papergen.py crashed: " + (p.stderr.strip()[-200:] or "?")); sys.exit(1)
    tex = os.path.join(gdir, "test_paper.tex")
    if not os.path.exists(tex):
        print("FAIL: test_paper.tex not produced"); sys.exit(1)
    items = re.findall(r"\\item\s*\$(.+?)\$", open(tex, encoding="utf-8").read())
    n, distinct = len(items), len(set(items))
    if n < 10:
        print("FAIL: only %d question items (expected >=10)" % n); sys.exit(1)
    if distinct < max(8, int(n * 0.6)):
        print("FAIL: questions still repeating: %d distinct of %d" % (distinct, n)); sys.exit(1)
    print("RW1 OK: %d items, %d distinct" % (n, distinct))

if __name__ == "__main__":
    main()
