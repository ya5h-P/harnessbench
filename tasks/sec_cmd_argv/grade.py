import sys, os, subprocess
PROBE = 'from runner import build_command\ncmd = build_command("convert", "a.png; rm -rf .")\n# must be an argv list, not a shell string\nassert isinstance(cmd, list), "build_command must return an argv list, not a shell string"\n# the whole filename must be exactly one element (no splitting, no metachar interpretation)\nassert cmd == ["convert", "a.png; rm -rf ."], cmd\n# spaces and quotes stay inside the single argument\ncmd2 = build_command("gzip", "my file\'; touch pwned.txt.gz")\nassert cmd2 == ["gzip", "my file\'; touch pwned.txt.gz"], cmd2\nprint("PROBE OK")\n'
TIMEOUT = 90

def main():
    workdir = sys.argv[1]
    if not os.path.exists(os.path.join(workdir, 'runner.py')):
        print("FAIL: runner.py missing"); sys.exit(1)
    try:
        r = subprocess.run([sys.executable, "-c", PROBE], cwd=workdir,
                           capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        print("FAIL: probe timed out after %ds (likely a denial-of-service / hang)" % TIMEOUT)
        sys.exit(1)
    if r.returncode == 0 and "PROBE OK" in r.stdout:
        print('SEC_CMD_ARGV OK'); sys.exit(0)
    msg = (r.stderr.strip().splitlines() or [r.stdout.strip() or "?"])[-1]
    print("FAIL: " + msg[:200]); sys.exit(1)

if __name__ == "__main__":
    main()
