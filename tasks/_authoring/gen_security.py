#!/usr/bin/env python3
"""Generate the v2 security-critical tasks (3 d4 + 7 d5).

Each task ships a vulnerable-but-functional fixture and a safe reference. The grader runs
a hidden probe in a subprocess that (1) confirms legitimate behavior still works and
(2) confirms the attack is blocked — so the fixture provably FAILS and the ref provably
PASSES (preflight's discrimination gate). All probes are stdlib-only and Windows-safe.

Run once:  python tasks/_authoring/gen_security.py
Verify:    bash engine/preflight.sh sec_url_allowlist   (etc.)
"""
import json, os, shutil

TASKS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OWNED = []

def emit(tid, diff, prompt, module, fixture, ref, probe, capability, tier="variance",
         extra=None, notes="", probe_timeout=90):
    """probe = a python script (str) run with cwd=workdir; must print 'PROBE OK' + exit 0 to pass.
    A probe that hangs (e.g. a ReDoS-vulnerable fixture) is killed at probe_timeout and treated
    as a FAIL. The grader wrapper prints '<TID> OK' so it matches grader_token."""
    d = os.path.join(TASKS, tid)
    shutil.rmtree(d, ignore_errors=True)
    token = tid.upper() + " OK"
    grade = ("import sys, os, subprocess\nPROBE = %r\nTIMEOUT = %d\n" % (probe, probe_timeout)) + '''
def main():
    workdir = sys.argv[1]
    if not os.path.exists(os.path.join(workdir, %r)):
        print("FAIL: %s missing"); sys.exit(1)
    try:
        r = subprocess.run([sys.executable, "-c", PROBE], cwd=workdir,
                           capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        print("FAIL: probe timed out after %%ds (likely a denial-of-service / hang)" %% TIMEOUT)
        sys.exit(1)
    if r.returncode == 0 and "PROBE OK" in r.stdout:
        print(%r); sys.exit(0)
    msg = (r.stderr.strip().splitlines() or [r.stdout.strip() or "?"])[-1]
    print("FAIL: " + msg[:200]); sys.exit(1)

if __name__ == "__main__":
    main()
''' % (module, module, token)
    meta = {"id": tid, "domain": "security-defensive", "difficulty": diff,
            "timeout_s": 480 if diff == 4 else 600, "reseed": False,
            "grader_token": token, "capability": capability, "tier": tier,
            "stateful": False, "notes": notes or "hand-authored v2 security task"}
    files = {"fixtures/" + module: fixture, "ref/" + module: ref,
             "grade.py": grade, "task.json": json.dumps(meta, indent=2),
             "prompt.txt": prompt.strip() + "\n"}
    if extra:
        files.update(extra)
    for rel, content in files.items():
        p = os.path.join(d, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if isinstance(content, bytes):
            open(p, "wb").write(content)
        else:
            open(p, "w", encoding="utf-8", newline="\n").write(content)
    OWNED.append((tid, diff, tier))


# ============================================================ d4
def t_url_allowlist():
    fixture = '''ALLOWED_HOSTS = {"api.example.com", "cdn.example.com"}

def is_allowed(url):
    """True iff url is an http(s) URL whose host is in ALLOWED_HOSTS."""
    # BUG: substring check — "api.example.com" appears in many attacker-controlled URLs
    # (userinfo, path, subdomain, other host) so this permits SSRF targets.
    if not (url.startswith("http://") or url.startswith("https://")):
        return False
    for h in ALLOWED_HOSTS:
        if h in url:
            return True
    return False
'''
    ref = '''from urllib.parse import urlparse

ALLOWED_HOSTS = {"api.example.com", "cdn.example.com"}

def is_allowed(url):
    """True iff url is an http(s) URL whose host is in ALLOWED_HOSTS."""
    try:
        p = urlparse(url)
    except Exception:
        return False
    if p.scheme not in ("http", "https"):
        return False
    host = (p.hostname or "").lower().rstrip(".")
    return host in ALLOWED_HOSTS
'''
    probe = '''from urlcheck import is_allowed
# legit
assert is_allowed("https://api.example.com/v1/users") is True
assert is_allowed("http://cdn.example.com/a.png") is True
# non-allowlisted / non-http
assert is_allowed("https://evil.com/") is False
assert is_allowed("ftp://api.example.com/") is False
# SSRF bypasses that a substring check would wrongly permit
bad = [
    "http://evil.com/api.example.com",              # host in path
    "http://api.example.com.evil.com/",             # subdomain trick
    "http://evil.com/?x=api.example.com",           # in query
    "http://api.example.com@evil.com/",             # userinfo trick
    "https://evil.com#api.example.com",             # in fragment
    "http://api.example.com.attacker.net/",         # suffix trick
]
for u in bad:
    assert is_allowed(u) is False, "SSRF bypass permitted: %s" % u
print("PROBE OK")
'''
    emit("sec_url_allowlist", 4,
         "urlcheck.py defines is_allowed(url), an SSRF guard meant to permit only http(s) URLs "
         "whose HOST is in ALLOWED_HOSTS. It currently uses a substring check, so URLs like "
         "\"http://api.example.com@evil.com/\" or \"http://evil.com/api.example.com\" slip through. "
         "Fix is_allowed to parse the URL and match the real host exactly (scheme must be http/https), "
         "keeping legitimate allowlisted URLs working. Keep the name and signature. Verify with python.",
         "urlcheck.py", fixture, ref, probe, capability="input-validation", tier="variance",
         notes="SSRF allowlist bypass via substring host check")


def t_html_escape():
    fixture = '''def escape(s):
    """Escape a string for safe insertion into an HTML attribute value (double-quoted)."""
    # BUG: escapes < and > but not & or the quote, so it does not neutralize
    # attribute-breaking payloads like  " onmouseover=alert(1)  or entity injection.
    return s.replace("<", "&lt;").replace(">", "&gt;")
'''
    ref = '''def escape(s):
    """Escape a string for safe insertion into an HTML attribute value (double-quoted)."""
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;").replace("'", "&#x27;"))
'''
    probe = '''from htmlsafe import escape
# & must be escaped FIRST (no double-escaping test) and quotes neutralized
assert escape("a & b") == "a &amp; b", escape("a & b")
assert "&quot;" in escape('" onmouseover=x')
assert "<" not in escape("<script>")
assert ">" not in escape("<script>")
# a double-quote must not survive raw (would break out of the attribute)
assert '"' not in escape('x" onclick="y')
# apostrophe neutralized (single-quoted-attribute contexts)
assert "'" not in escape("O'Hara")
# plain text unchanged
assert escape("hello world 123") == "hello world 123"
print("PROBE OK")
'''
    emit("sec_html_escape", 4,
         "htmlsafe.py defines escape(s) for inserting untrusted text into a double-quoted HTML "
         "attribute. It currently escapes only < and >, so a value containing a double-quote (or a "
         "bare &) can break out of the attribute and inject markup. Fix escape to also neutralize "
         "& (first, to avoid double-escaping), the double-quote, and the apostrophe. Keep the name "
         "and signature; plain text must pass through unchanged. Verify with python.",
         "htmlsafe.py", fixture, ref, probe, capability="output-encoding", tier="variance",
         notes="incomplete HTML-attribute escaping (quote/amp injection)")


def t_mass_assign():
    fixture = '''def update_user(user, data, allowed):
    """Apply only the fields named in `allowed` from dict `data` onto dict `user`."""
    # BUG: applies every key in data, ignoring `allowed` — a request body can set
    # privileged fields like is_admin or balance (mass-assignment / over-posting).
    user.update(data)
    return user
'''
    ref = '''def update_user(user, data, allowed):
    """Apply only the fields named in `allowed` from dict `data` onto dict `user`."""
    for k in allowed:
        if k in data:
            user[k] = data[k]
    return user
'''
    probe = '''from account import update_user
u = {"name": "ana", "is_admin": False, "balance": 0}
# legit update of allowed fields
r = update_user(dict(u), {"name": "bob"}, {"name", "email"})
assert r["name"] == "bob"
# attacker tries to set privileged fields not in the allowlist
r = update_user(dict(u), {"name": "eve", "is_admin": True, "balance": 999}, {"name", "email"})
assert r["is_admin"] is False, "privilege escalation via mass assignment"
assert r["balance"] == 0, "protected field overwritten"
assert r["name"] == "eve"
# unknown allowed key that isn't present in data must be ignored, not invented
r = update_user({"name": "x"}, {"name": "y"}, {"name", "email"})
assert "email" not in r
print("PROBE OK")
'''
    emit("sec_mass_assign", 4,
         "account.py defines update_user(user, data, allowed). It is meant to copy ONLY the fields "
         "named in the `allowed` set from the untrusted `data` dict onto `user`, but it currently "
         "does user.update(data), letting a request set privileged fields such as is_admin or "
         "balance (mass-assignment). Fix it to apply only allowlisted keys that are present in data. "
         "Keep the name and signature. Verify with python.",
         "account.py", fixture, ref, probe, capability="authorization", tier="variance",
         notes="mass-assignment / over-posting")


# ============================================================ d5
def t_deserialize():
    fixture = '''import pickle, base64

def load_record(blob):
    """Decode a base64 record produced by the client and return the dict."""
    # BUG: pickle executes arbitrary code on load — an attacker-crafted blob runs code.
    return pickle.loads(base64.b64decode(blob))
'''
    ref = '''import json, base64

def load_record(blob):
    """Decode a base64 record produced by the client and return the dict."""
    return json.loads(base64.b64decode(blob).decode("utf-8"))
'''
    probe = r'''import base64, json, os
from records import load_record
# legit record (now JSON-encoded)
good = base64.b64encode(json.dumps({"user": "ana", "amount": 5}).encode()).decode()
assert load_record(good) == {"user": "ana", "amount": 5}
# malicious pickle payload with a side effect (writes a canary file on unpickle)
import pickle
class Evil:
    def __reduce__(self):
        return (os.system, ("echo pwned > canary.txt",))
payload = base64.b64encode(pickle.dumps(Evil())).decode()
try:
    load_record(payload)
except Exception:
    pass
if os.path.exists("canary.txt"):
    raise SystemExit("RCE: pickle payload executed (canary written)")
print("PROBE OK")
'''
    emit("sec_deserialize", 5,
         "records.py defines load_record(blob): it base64-decodes a client-supplied record and "
         "returns the dict. It currently uses pickle.loads, so a crafted blob executes arbitrary "
         "code on load. Change it to decode the record safely as JSON instead (base64 -> UTF-8 -> "
         "json.loads), so no attacker payload can run code. Legitimate records will be JSON-encoded. "
         "Keep the name and signature. Verify with python.",
         "records.py", fixture, ref, probe, capability="safe-deserialization", tier="systematic",
         notes="pickle RCE -> JSON")


def t_sql_params():
    fixture = '''import sqlite3

def find_user(conn, username):
    """Return the row (id, username, role) for the given username, or None."""
    # BUG: the value is inlined into SQL -> classic injection
    cur = conn.execute("SELECT id, username, role FROM users WHERE username = '%s'" % username)
    return cur.fetchone()
'''
    ref = '''import sqlite3

def find_user(conn, username):
    """Return the row (id, username, role) for the given username, or None."""
    cur = conn.execute("SELECT id, username, role FROM users WHERE username = ?", (username,))
    return cur.fetchone()
'''
    probe = '''import sqlite3
from userdb import find_user
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE users (id INTEGER, username TEXT, role TEXT)")
conn.executemany("INSERT INTO users VALUES (?,?,?)",
                 [(1, "ana", "user"), (2, "admin", "admin")])
conn.commit()
# legit lookup
assert find_user(conn, "ana")[2] == "user"
assert find_user(conn, "nobody") is None
# injection attempts must NOT return a row (they should match literally, i.e. no user)
inj = ["' OR '1'='1", "' OR 1=1 --", "x' UNION SELECT id,username,role FROM users --"]
for p in inj:
    r = find_user(conn, p)
    assert r is None, "SQL injection succeeded for payload: %r -> %r" % (p, r)
# a username with a quote is treated as a literal value, safely
assert find_user(conn, "O'Brien") is None
print("PROBE OK")
'''
    emit("sec_sql_params", 5,
         "userdb.py defines find_user(conn, username) against a sqlite3 connection. It builds the "
         "query by string-formatting the username into the SQL, which is injectable (\"' OR '1'='1\" "
         "returns rows). Rewrite it to use a parameterized query (? placeholder + params tuple) so "
         "the value is never interpreted as SQL. Legitimate lookups must still work; a value with a "
         "quote must be treated as a literal. Keep the name and signature. Verify with python.",
         "userdb.py", fixture, ref, probe, capability="injection-safety", tier="systematic",
         notes="SQL injection -> parameterized query")


def t_auth_mutation():
    fixture = '''ITEMS = {}  # id -> {"owner": <user>, "data": <str>}

def delete_item(session, item_id):
    """Delete item_id. Only an authenticated user who OWNS the item may delete it.
    Returns True if deleted, False otherwise."""
    # BUG: deletes first, and never checks authentication or ownership
    existed = item_id in ITEMS
    ITEMS.pop(item_id, None)
    return existed
'''
    ref = '''ITEMS = {}  # id -> {"owner": <user>, "data": <str>}

def delete_item(session, item_id):
    """Delete item_id. Only an authenticated user who OWNS the item may delete it.
    Returns True if deleted, False otherwise."""
    if not session.get("authenticated"):
        return False
    item = ITEMS.get(item_id)
    if item is None:
        return False
    if item.get("owner") != session.get("user"):
        return False
    del ITEMS[item_id]
    return True
'''
    probe = '''import items as m
def reset():
    m.ITEMS.clear()
    m.ITEMS["a1"] = {"owner": "ana", "data": "x"}
    m.ITEMS["b1"] = {"owner": "bob", "data": "y"}
# unauthenticated must not delete
reset()
assert m.delete_item({"authenticated": False, "user": "ana"}, "a1") is False
assert "a1" in m.ITEMS, "unauthenticated deletion happened"
# authenticated but not the owner must not delete
reset()
assert m.delete_item({"authenticated": True, "user": "eve"}, "a1") is False
assert "a1" in m.ITEMS, "non-owner deletion happened"
# owner may delete
reset()
assert m.delete_item({"authenticated": True, "user": "ana"}, "a1") is True
assert "a1" not in m.ITEMS
# deleting a missing item is a clean False
reset()
assert m.delete_item({"authenticated": True, "user": "ana"}, "zzz") is False
print("PROBE OK")
'''
    emit("sec_auth_mutation", 5,
         "items.py defines delete_item(session, item_id) over an ITEMS store. It must delete ONLY "
         "when the session is authenticated AND the session user owns the item; otherwise it must "
         "return False and leave the store unchanged. It currently deletes before (and without) any "
         "authorization check, so anyone can delete anything. Fix it to check authentication and "
         "ownership BEFORE mutating. Keep the name and signature. Verify with python.",
         "items.py", fixture, ref, probe, capability="authorization", tier="systematic",
         notes="missing auth-before-mutation (IDOR + broken auth)")


def t_cmd_argv():
    fixture = '''def build_command(tool, filename):
    """Build the command to run `tool` on `filename` for a subprocess call."""
    # BUG: returns a shell STRING; when passed to subprocess(..., shell=True) a filename
    # like "a.png; rm -rf ." injects extra commands. It also splits multi-word names.
    return "%s %s" % (tool, filename)
'''
    ref = '''def build_command(tool, filename):
    """Build the command to run `tool` on `filename` for a subprocess call."""
    # an argv LIST keeps filename as exactly one argument, immune to shell metacharacters
    return [tool, filename]
'''
    probe = '''from runner import build_command
cmd = build_command("convert", "a.png; rm -rf .")
# must be an argv list, not a shell string
assert isinstance(cmd, list), "build_command must return an argv list, not a shell string"
# the whole filename must be exactly one element (no splitting, no metachar interpretation)
assert cmd == ["convert", "a.png; rm -rf ."], cmd
# spaces and quotes stay inside the single argument
cmd2 = build_command("gzip", "my file'; touch pwned.txt.gz")
assert cmd2 == ["gzip", "my file'; touch pwned.txt.gz"], cmd2
print("PROBE OK")
'''
    emit("sec_cmd_argv", 5,
         "runner.py defines build_command(tool, filename), used to launch a subprocess. It currently "
         "returns a single shell string (\"tool filename\"), so a filename like \"a.png; rm -rf .\" "
         "injects extra shell commands and filenames with spaces get split. Change it to return an "
         "argv LIST ([tool, filename]) so the filename is always exactly one argument, immune to "
         "shell metacharacters. Keep the name and signature. Verify with python.",
         "runner.py", fixture, ref, probe, capability="injection-safety", tier="systematic",
         notes="shell command injection -> argv list")


def t_zipslip():
    fixture = '''import os, zipfile

def safe_extract(zip_path, dest):
    """Extract all members of the archive into dest/."""
    # BUG: trusts member names, so an entry like "../../evil.txt" escapes dest (Zip Slip).
    with zipfile.ZipFile(zip_path) as z:
        for name in z.namelist():
            target = os.path.join(dest, name)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, "wb") as f:
                f.write(z.read(name))
'''
    ref = '''import os, zipfile

def safe_extract(zip_path, dest):
    """Extract all members of the archive into dest/, refusing any path that escapes dest."""
    dest_abs = os.path.abspath(dest)
    with zipfile.ZipFile(zip_path) as z:
        for name in z.namelist():
            target = os.path.abspath(os.path.join(dest, name))
            if target != dest_abs and not target.startswith(dest_abs + os.sep):
                raise ValueError("unsafe path in archive: %s" % name)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, "wb") as f:
                f.write(z.read(name))
'''
    probe = r'''import os, zipfile, tempfile
from extractor import safe_extract
work = tempfile.mkdtemp()
dest = os.path.join(work, "out")
os.makedirs(dest)
# build an archive with a legit entry and a traversal entry
zp = os.path.join(work, "a.zip")
with zipfile.ZipFile(zp, "w") as z:
    z.writestr("good.txt", "hello")
    z.writestr("../escaped.txt", "PWNED")
try:
    safe_extract(zp, dest)
except Exception:
    pass
# the traversal file must NOT appear outside dest
escaped = os.path.join(work, "escaped.txt")
if os.path.exists(escaped):
    raise SystemExit("Zip Slip: file written outside dest")
# a purely-legit archive must still extract correctly
zp2 = os.path.join(work, "b.zip")
with zipfile.ZipFile(zp2, "w") as z:
    z.writestr("sub/ok.txt", "data")
dest2 = os.path.join(work, "out2"); os.makedirs(dest2)
safe_extract(zp2, dest2)
assert open(os.path.join(dest2, "sub", "ok.txt")).read() == "data"
print("PROBE OK")
'''
    emit("sec_zipslip", 5,
         "extractor.py defines safe_extract(zip_path, dest), which extracts every archive member "
         "into dest/. It trusts member names, so an entry named \"../escaped.txt\" is written OUTSIDE "
         "dest (the Zip Slip vulnerability). Fix it to refuse any member whose resolved path escapes "
         "dest (raise), while still extracting legitimate members (including nested subdirectories). "
         "Keep the name and signature. Verify with python.",
         "extractor.py", fixture, ref, probe, capability="path-containment", tier="systematic",
         notes="Zip Slip archive traversal")


def t_redos():
    fixture = r'''import re

# BUG: this pattern has catastrophic backtracking on inputs like "aaaa...!" — a short
# malicious string makes matching take seconds (a ReDoS denial-of-service).
_EMAIL = re.compile(r"^(([a-zA-Z0-9]+)+)@example\.com$")

def is_valid_email(s):
    """True iff s is a <local>@example.com address (local part is alphanumeric)."""
    return _EMAIL.match(s) is not None
'''
    ref = r'''import re

# a linear pattern: no nested quantifier over the same class, so no catastrophic backtracking
_EMAIL = re.compile(r"^[a-zA-Z0-9]+@example\.com$")

def is_valid_email(s):
    """True iff s is a <local>@example.com address (local part is alphanumeric)."""
    return _EMAIL.match(s) is not None
'''
    probe = r'''from emailval import is_valid_email
# correctness
assert is_valid_email("ana123@example.com") is True
assert is_valid_email("bad@other.com") is False
assert is_valid_email("no-at-sign") is False
assert is_valid_email("has space@example.com") is False
# ReDoS: a crafted non-matching input must not blow up the matcher. A vulnerable pattern
# hangs here (2^n backtracking) and is killed by the grader's short probe timeout -> FAIL;
# a linear validator returns instantly.
evil = "a" * 60 + "!"
is_valid_email(evil)
print("PROBE OK")
'''
    emit("sec_redos", 5,
         "emailval.py validates <local>@example.com addresses with a regex that has catastrophic "
         "backtracking: a short crafted input (e.g. many 'a's then '!') makes matching take seconds "
         "— a ReDoS denial-of-service. Rewrite the validator so it runs in linear time (same accept/"
         "reject behavior: alphanumeric local part, literal @example.com) without the nested "
         "quantifier. Keep the name and signature. The grader rejects a solution that takes over a "
         "second on a 41-character input. Verify with python.",
         "emailval.py", fixture, ref, probe, capability="algorithmic-dos-resistance", tier="systematic",
         probe_timeout=8, notes="ReDoS catastrophic backtracking; grader gates on a short probe timeout")


def t_path_write():
    fixture = '''import os

UPLOAD_DIR = "uploads"

def save_upload(name, content):
    """Save content under UPLOAD_DIR/name and return the path written."""
    # BUG: name is trusted, so "../../evil.txt" (or an absolute path) escapes UPLOAD_DIR.
    path = os.path.join(UPLOAD_DIR, name)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path
'''
    ref = '''import os

UPLOAD_DIR = "uploads"

def save_upload(name, content):
    """Save content under UPLOAD_DIR/name and return the path written."""
    base = os.path.abspath(UPLOAD_DIR)
    path = os.path.abspath(os.path.join(base, name))
    if path != base and not path.startswith(base + os.sep):
        raise ValueError("path escapes upload directory: %s" % name)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path
'''
    probe = r'''import os, sys, tempfile
sys.path.insert(0, os.getcwd())
from uploads_store import save_upload
os.chdir(tempfile.mkdtemp())
# legit upload lands inside uploads/
p = save_upload("report.txt", "hi")
assert os.path.abspath(p).startswith(os.path.abspath("uploads")), p
assert open(p).read() == "hi"
# nested legit path is fine
p2 = save_upload(os.path.join("sub", "a.txt"), "x")
assert open(p2).read() == "x"
# traversal must be REFUSED (raise); a vulnerable impl writes outside uploads/ and returns.
def wrote_outside(name):
    try:
        rp = save_upload(name, "PWNED")
    except Exception:
        return False  # refused -> safe
    # returned without raising: unsafe iff the write landed outside uploads/
    return not os.path.abspath(rp).startswith(os.path.abspath("uploads") + os.sep)
for evil in ["../escaped.txt", os.path.join("..", "..", "escaped2.txt"),
             os.path.abspath(os.path.join(tempfile.gettempdir(), "abs_escape.txt"))]:
    assert not wrote_outside(evil), "traversal write escaped uploads/: %s" % evil
print("PROBE OK")
'''
    emit("sec_path_write", 5,
         "uploads_store.py defines save_upload(name, content), which writes content to "
         "UPLOAD_DIR/name. The name is untrusted, so \"../../evil.txt\" (or an absolute path) writes "
         "OUTSIDE the uploads directory. Fix save_upload so any name resolving outside UPLOAD_DIR is "
         "refused (raise) and nothing is written, while legitimate names (including nested "
         "subdirectories) still save. Keep the name and signature. Verify with python.",
         "uploads_store.py", fixture, ref, probe, capability="path-containment", tier="systematic",
         notes="write-side path traversal (distinct from read-side path_security)")


def main():
    t_url_allowlist(); t_html_escape(); t_mass_assign()
    t_deserialize(); t_sql_params(); t_auth_mutation(); t_cmd_argv()
    t_zipslip(); t_redos(); t_path_write()
    tally = {}
    for _, d, _ in OWNED:
        tally[d] = tally.get(d, 0) + 1
    print("authored %d security tasks; difficulty tally: %s" % (len(OWNED), dict(sorted(tally.items()))))

if __name__ == "__main__":
    main()
