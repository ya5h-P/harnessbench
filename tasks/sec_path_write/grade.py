import sys, os, subprocess
PROBE = 'import os, sys, tempfile\nsys.path.insert(0, os.getcwd())\nfrom uploads_store import save_upload\nos.chdir(tempfile.mkdtemp())\n# legit upload lands inside uploads/\np = save_upload("report.txt", "hi")\nassert os.path.abspath(p).startswith(os.path.abspath("uploads")), p\nassert open(p).read() == "hi"\n# nested legit path is fine\np2 = save_upload(os.path.join("sub", "a.txt"), "x")\nassert open(p2).read() == "x"\n# traversal must be REFUSED (raise); a vulnerable impl writes outside uploads/ and returns.\ndef wrote_outside(name):\n    try:\n        rp = save_upload(name, "PWNED")\n    except Exception:\n        return False  # refused -> safe\n    # returned without raising: unsafe iff the write landed outside uploads/\n    return not os.path.abspath(rp).startswith(os.path.abspath("uploads") + os.sep)\nfor evil in ["../escaped.txt", os.path.join("..", "..", "escaped2.txt"),\n             os.path.abspath(os.path.join(tempfile.gettempdir(), "abs_escape.txt"))]:\n    assert not wrote_outside(evil), "traversal write escaped uploads/: %s" % evil\nprint("PROBE OK")\n'
TIMEOUT = 90

def main():
    workdir = sys.argv[1]
    if not os.path.exists(os.path.join(workdir, 'uploads_store.py')):
        print("FAIL: uploads_store.py missing"); sys.exit(1)
    try:
        r = subprocess.run([sys.executable, "-c", PROBE], cwd=workdir,
                           capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        print("FAIL: probe timed out after %ds (likely a denial-of-service / hang)" % TIMEOUT)
        sys.exit(1)
    if r.returncode == 0 and "PROBE OK" in r.stdout:
        print('SEC_PATH_WRITE OK'); sys.exit(0)
    msg = (r.stderr.strip().splitlines() or [r.stdout.strip() or "?"])[-1]
    print("FAIL: " + msg[:200]); sys.exit(1)

if __name__ == "__main__":
    main()
