import sys, os, subprocess
PROBE = 'import items as m\ndef reset():\n    m.ITEMS.clear()\n    m.ITEMS["a1"] = {"owner": "ana", "data": "x"}\n    m.ITEMS["b1"] = {"owner": "bob", "data": "y"}\n# unauthenticated must not delete\nreset()\nassert m.delete_item({"authenticated": False, "user": "ana"}, "a1") is False\nassert "a1" in m.ITEMS, "unauthenticated deletion happened"\n# authenticated but not the owner must not delete\nreset()\nassert m.delete_item({"authenticated": True, "user": "eve"}, "a1") is False\nassert "a1" in m.ITEMS, "non-owner deletion happened"\n# owner may delete\nreset()\nassert m.delete_item({"authenticated": True, "user": "ana"}, "a1") is True\nassert "a1" not in m.ITEMS\n# deleting a missing item is a clean False\nreset()\nassert m.delete_item({"authenticated": True, "user": "ana"}, "zzz") is False\nprint("PROBE OK")\n'
TIMEOUT = 90

def main():
    workdir = sys.argv[1]
    if not os.path.exists(os.path.join(workdir, 'items.py')):
        print("FAIL: items.py missing"); sys.exit(1)
    try:
        r = subprocess.run([sys.executable, "-c", PROBE], cwd=workdir,
                           capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        print("FAIL: probe timed out after %ds (likely a denial-of-service / hang)" % TIMEOUT)
        sys.exit(1)
    if r.returncode == 0 and "PROBE OK" in r.stdout:
        print('SEC_AUTH_MUTATION OK'); sys.exit(0)
    msg = (r.stderr.strip().splitlines() or [r.stdout.strip() or "?"])[-1]
    print("FAIL: " + msg[:200]); sys.exit(1)

if __name__ == "__main__":
    main()
