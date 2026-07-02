import sys, os, shutil, subprocess, tempfile

def main():
    workdir, gradedir = sys.argv[1], sys.argv[2]
    modfile = "textkit_3.py"
    src = os.path.join(workdir, modfile)
    if not os.path.exists(src):
        print("FAIL: %s missing" % modfile); sys.exit(1)
    tmp = tempfile.mkdtemp(prefix="hbtf_")
    shutil.copy(src, os.path.join(tmp, modfile))
    shutil.copy(os.path.join(gradedir, "tests_hidden.py"), os.path.join(tmp, "tests_hidden.py"))
    r = subprocess.run([sys.executable, "tests_hidden.py"], cwd=tmp,
                       capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        tail = (r.stdout + r.stderr).strip().splitlines()[-1:] or ["?"]
        print("FAIL: hidden tests failed: %s" % tail[0]); sys.exit(1)
    print("TESTFIX_03 OK")

if __name__ == "__main__":
    main()
