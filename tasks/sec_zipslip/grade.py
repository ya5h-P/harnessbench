import sys, os, subprocess
PROBE = 'import os, zipfile, tempfile\nfrom extractor import safe_extract\nwork = tempfile.mkdtemp()\ndest = os.path.join(work, "out")\nos.makedirs(dest)\n# build an archive with a legit entry and a traversal entry\nzp = os.path.join(work, "a.zip")\nwith zipfile.ZipFile(zp, "w") as z:\n    z.writestr("good.txt", "hello")\n    z.writestr("../escaped.txt", "PWNED")\ntry:\n    safe_extract(zp, dest)\nexcept Exception:\n    pass\n# the traversal file must NOT appear outside dest\nescaped = os.path.join(work, "escaped.txt")\nif os.path.exists(escaped):\n    raise SystemExit("Zip Slip: file written outside dest")\n# a purely-legit archive must still extract correctly\nzp2 = os.path.join(work, "b.zip")\nwith zipfile.ZipFile(zp2, "w") as z:\n    z.writestr("sub/ok.txt", "data")\ndest2 = os.path.join(work, "out2"); os.makedirs(dest2)\nsafe_extract(zp2, dest2)\nassert open(os.path.join(dest2, "sub", "ok.txt")).read() == "data"\nprint("PROBE OK")\n'
TIMEOUT = 90

def main():
    workdir = sys.argv[1]
    if not os.path.exists(os.path.join(workdir, 'extractor.py')):
        print("FAIL: extractor.py missing"); sys.exit(1)
    try:
        r = subprocess.run([sys.executable, "-c", PROBE], cwd=workdir,
                           capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        print("FAIL: probe timed out after %ds (likely a denial-of-service / hang)" % TIMEOUT)
        sys.exit(1)
    if r.returncode == 0 and "PROBE OK" in r.stdout:
        print('SEC_ZIPSLIP OK'); sys.exit(0)
    msg = (r.stderr.strip().splitlines() or [r.stdout.strip() or "?"])[-1]
    print("FAIL: " + msg[:200]); sys.exit(1)

if __name__ == "__main__":
    main()
