import sys, os, subprocess
PROBE = 'from htmlsafe import escape\n# & must be escaped FIRST (no double-escaping test) and quotes neutralized\nassert escape("a & b") == "a &amp; b", escape("a & b")\nassert "&quot;" in escape(\'" onmouseover=x\')\nassert "<" not in escape("<script>")\nassert ">" not in escape("<script>")\n# a double-quote must not survive raw (would break out of the attribute)\nassert \'"\' not in escape(\'x" onclick="y\')\n# apostrophe neutralized (single-quoted-attribute contexts)\nassert "\'" not in escape("O\'Hara")\n# plain text unchanged\nassert escape("hello world 123") == "hello world 123"\nprint("PROBE OK")\n'
TIMEOUT = 90

def main():
    workdir = sys.argv[1]
    if not os.path.exists(os.path.join(workdir, 'htmlsafe.py')):
        print("FAIL: htmlsafe.py missing"); sys.exit(1)
    try:
        r = subprocess.run([sys.executable, "-c", PROBE], cwd=workdir,
                           capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        print("FAIL: probe timed out after %ds (likely a denial-of-service / hang)" % TIMEOUT)
        sys.exit(1)
    if r.returncode == 0 and "PROBE OK" in r.stdout:
        print('SEC_HTML_ESCAPE OK'); sys.exit(0)
    msg = (r.stderr.strip().splitlines() or [r.stdout.strip() or "?"])[-1]
    print("FAIL: " + msg[:200]); sys.exit(1)

if __name__ == "__main__":
    main()
