import sys, os, subprocess
PROBE = 'import sqlite3\nfrom userdb import find_user\nconn = sqlite3.connect(":memory:")\nconn.execute("CREATE TABLE users (id INTEGER, username TEXT, role TEXT)")\nconn.executemany("INSERT INTO users VALUES (?,?,?)",\n                 [(1, "ana", "user"), (2, "admin", "admin")])\nconn.commit()\n# legit lookup\nassert find_user(conn, "ana")[2] == "user"\nassert find_user(conn, "nobody") is None\n# injection attempts must NOT return a row (they should match literally, i.e. no user)\ninj = ["\' OR \'1\'=\'1", "\' OR 1=1 --", "x\' UNION SELECT id,username,role FROM users --"]\nfor p in inj:\n    r = find_user(conn, p)\n    assert r is None, "SQL injection succeeded for payload: %r -> %r" % (p, r)\n# a username with a quote is treated as a literal value, safely\nassert find_user(conn, "O\'Brien") is None\nprint("PROBE OK")\n'
TIMEOUT = 90

def main():
    workdir = sys.argv[1]
    if not os.path.exists(os.path.join(workdir, 'userdb.py')):
        print("FAIL: userdb.py missing"); sys.exit(1)
    try:
        r = subprocess.run([sys.executable, "-c", PROBE], cwd=workdir,
                           capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        print("FAIL: probe timed out after %ds (likely a denial-of-service / hang)" % TIMEOUT)
        sys.exit(1)
    if r.returncode == 0 and "PROBE OK" in r.stdout:
        print('SEC_SQL_PARAMS OK'); sys.exit(0)
    msg = (r.stderr.strip().splitlines() or [r.stdout.strip() or "?"])[-1]
    print("FAIL: " + msg[:200]); sys.exit(1)

if __name__ == "__main__":
    main()
