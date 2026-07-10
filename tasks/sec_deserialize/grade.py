import sys, os, subprocess
PROBE = 'import base64, json, os\nfrom records import load_record\n# legit record (now JSON-encoded)\ngood = base64.b64encode(json.dumps({"user": "ana", "amount": 5}).encode()).decode()\nassert load_record(good) == {"user": "ana", "amount": 5}\n# malicious pickle payload with a side effect (writes a canary file on unpickle)\nimport pickle\nclass Evil:\n    def __reduce__(self):\n        return (os.system, ("echo pwned > canary.txt",))\npayload = base64.b64encode(pickle.dumps(Evil())).decode()\ntry:\n    load_record(payload)\nexcept Exception:\n    pass\nif os.path.exists("canary.txt"):\n    raise SystemExit("RCE: pickle payload executed (canary written)")\nprint("PROBE OK")\n'
TIMEOUT = 90

def main():
    workdir = sys.argv[1]
    if not os.path.exists(os.path.join(workdir, 'records.py')):
        print("FAIL: records.py missing"); sys.exit(1)
    try:
        r = subprocess.run([sys.executable, "-c", PROBE], cwd=workdir,
                           capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        print("FAIL: probe timed out after %ds (likely a denial-of-service / hang)" % TIMEOUT)
        sys.exit(1)
    if r.returncode == 0 and "PROBE OK" in r.stdout:
        print('SEC_DESERIALIZE OK'); sys.exit(0)
    msg = (r.stderr.strip().splitlines() or [r.stdout.strip() or "?"])[-1]
    print("FAIL: " + msg[:200]); sys.exit(1)

if __name__ == "__main__":
    main()
