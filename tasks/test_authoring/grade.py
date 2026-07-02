import sys, os, shutil, subprocess, tempfile

def run_against(test_file, impl_file, tmp):
    os.makedirs(tmp, exist_ok=True)
    shutil.copy(test_file, os.path.join(tmp, "test_mathutils.py"))
    shutil.copy(impl_file, os.path.join(tmp, "mathutils.py"))
    r = subprocess.run([sys.executable, "test_mathutils.py"], cwd=tmp,
                       capture_output=True, text=True, timeout=60)
    return r.returncode

def main():
    workdir, gradedir = sys.argv[1], sys.argv[2]
    test_file = os.path.join(workdir, "test_mathutils.py")
    if not os.path.exists(test_file):
        print("FAIL: test_mathutils.py missing"); sys.exit(1)
    correct = os.path.join(gradedir, "mathutils_correct.py")
    buggy = os.path.join(gradedir, "mathutils_buggy.py")
    base = tempfile.mkdtemp(prefix="testauth_")

    rc_correct = run_against(test_file, correct, os.path.join(base, "c"))
    if rc_correct != 0:
        print("FAIL: the test suite fails even the CORRECT implementation (rc=%d)" % rc_correct); sys.exit(1)
    rc_buggy = run_against(test_file, buggy, os.path.join(base, "b"))
    if rc_buggy == 0:
        print("FAIL: the test suite does NOT catch the buggy implementation"); sys.exit(1)
    print("TESTAUTH OK")

if __name__ == "__main__":
    main()
