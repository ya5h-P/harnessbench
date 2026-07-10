import sys, os, subprocess
PROBE = 'from urlcheck import is_allowed\n# legit\nassert is_allowed("https://api.example.com/v1/users") is True\nassert is_allowed("http://cdn.example.com/a.png") is True\n# non-allowlisted / non-http\nassert is_allowed("https://evil.com/") is False\nassert is_allowed("ftp://api.example.com/") is False\n# SSRF bypasses that a substring check would wrongly permit\nbad = [\n    "http://evil.com/api.example.com",              # host in path\n    "http://api.example.com.evil.com/",             # subdomain trick\n    "http://evil.com/?x=api.example.com",           # in query\n    "http://api.example.com@evil.com/",             # userinfo trick\n    "https://evil.com#api.example.com",             # in fragment\n    "http://api.example.com.attacker.net/",         # suffix trick\n]\nfor u in bad:\n    assert is_allowed(u) is False, "SSRF bypass permitted: %s" % u\nprint("PROBE OK")\n'
TIMEOUT = 90

def main():
    workdir = sys.argv[1]
    if not os.path.exists(os.path.join(workdir, 'urlcheck.py')):
        print("FAIL: urlcheck.py missing"); sys.exit(1)
    try:
        r = subprocess.run([sys.executable, "-c", PROBE], cwd=workdir,
                           capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        print("FAIL: probe timed out after %ds (likely a denial-of-service / hang)" % TIMEOUT)
        sys.exit(1)
    if r.returncode == 0 and "PROBE OK" in r.stdout:
        print('SEC_URL_ALLOWLIST OK'); sys.exit(0)
    msg = (r.stderr.strip().splitlines() or [r.stdout.strip() or "?"])[-1]
    print("FAIL: " + msg[:200]); sys.exit(1)

if __name__ == "__main__":
    main()
