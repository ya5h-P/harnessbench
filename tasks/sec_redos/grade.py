import sys, os, subprocess
PROBE = 'from emailval import is_valid_email\n# correctness\nassert is_valid_email("ana123@example.com") is True\nassert is_valid_email("bad@other.com") is False\nassert is_valid_email("no-at-sign") is False\nassert is_valid_email("has space@example.com") is False\n# ReDoS: a crafted non-matching input must not blow up the matcher. A vulnerable pattern\n# hangs here (2^n backtracking) and is killed by the grader\'s short probe timeout -> FAIL;\n# a linear validator returns instantly.\nevil = "a" * 60 + "!"\nis_valid_email(evil)\nprint("PROBE OK")\n'
TIMEOUT = 8

def main():
    workdir = sys.argv[1]
    if not os.path.exists(os.path.join(workdir, 'emailval.py')):
        print("FAIL: emailval.py missing"); sys.exit(1)
    try:
        r = subprocess.run([sys.executable, "-c", PROBE], cwd=workdir,
                           capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        print("FAIL: probe timed out after %ds (likely a denial-of-service / hang)" % TIMEOUT)
        sys.exit(1)
    if r.returncode == 0 and "PROBE OK" in r.stdout:
        print('SEC_REDOS OK'); sys.exit(0)
    msg = (r.stderr.strip().splitlines() or [r.stdout.strip() or "?"])[-1]
    print("FAIL: " + msg[:200]); sys.exit(1)

if __name__ == "__main__":
    main()
