import sys, os, subprocess
PROBE = 'from account import update_user\nu = {"name": "ana", "is_admin": False, "balance": 0}\n# legit update of allowed fields\nr = update_user(dict(u), {"name": "bob"}, {"name", "email"})\nassert r["name"] == "bob"\n# attacker tries to set privileged fields not in the allowlist\nr = update_user(dict(u), {"name": "eve", "is_admin": True, "balance": 999}, {"name", "email"})\nassert r["is_admin"] is False, "privilege escalation via mass assignment"\nassert r["balance"] == 0, "protected field overwritten"\nassert r["name"] == "eve"\n# unknown allowed key that isn\'t present in data must be ignored, not invented\nr = update_user({"name": "x"}, {"name": "y"}, {"name", "email"})\nassert "email" not in r\nprint("PROBE OK")\n'
TIMEOUT = 90

def main():
    workdir = sys.argv[1]
    if not os.path.exists(os.path.join(workdir, 'account.py')):
        print("FAIL: account.py missing"); sys.exit(1)
    try:
        r = subprocess.run([sys.executable, "-c", PROBE], cwd=workdir,
                           capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        print("FAIL: probe timed out after %ds (likely a denial-of-service / hang)" % TIMEOUT)
        sys.exit(1)
    if r.returncode == 0 and "PROBE OK" in r.stdout:
        print('SEC_MASS_ASSIGN OK'); sys.exit(0)
    msg = (r.stderr.strip().splitlines() or [r.stdout.strip() or "?"])[-1]
    print("FAIL: " + msg[:200]); sys.exit(1)

if __name__ == "__main__":
    main()
