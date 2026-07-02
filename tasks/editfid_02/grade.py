import sys, os
def main():
    w = sys.argv[1]
    p = os.path.join(w, "settings.ini")
    if not os.path.exists(p): print("FAIL: settings.ini missing"); sys.exit(1)
    raw = open(p, "rb").read()
    if b"\n" in raw.replace(b"\r\n", b""): print("FAIL: bare LF found - CRLF not preserved"); sys.exit(1)
    txt = raw.decode("utf-8").replace("\r\n", "\n")
    want = dict(host="127.0.0.1", port="8443", retries="5", timeout_s="30", verify_tls="true")
    for k, v in want.items():
        if ("%s = %s" % (k, v)) not in txt: print("FAIL: %s should be %s" % (k, v)); sys.exit(1)
    print("EDITFID_02 OK")
main()
