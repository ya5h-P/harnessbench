import sys, os, subprocess

HIDDEN = r'''
import threading
from counter import Counter

THREADS, PER, TRIALS = 8, 250, 4
total = THREADS * PER
for trial in range(TRIALS):
    c = Counter()
    def work():
        for _ in range(PER):
            c.increment()
    ts = [threading.Thread(target=work) for _ in range(THREADS)]
    for t in ts: t.start()
    for t in ts: t.join()
    if c.value != total:
        raise SystemExit("lost updates: value=%d expected=%d (trial %d)" % (c.value, total, trial))
print("CONCURRENCY OK")
'''

def main():
    workdir = sys.argv[1]
    if not os.path.exists(os.path.join(workdir, "counter.py")):
        print("FAIL: counter.py missing"); sys.exit(1)
    r = subprocess.run([sys.executable, "-c", HIDDEN], cwd=workdir,
                       capture_output=True, text=True, timeout=120)
    if "CONCURRENCY OK" in r.stdout and r.returncode == 0:
        print("CONCURRENCY OK"); sys.exit(0)
    msg = (r.stderr.strip().splitlines() or ["?"])[-1]
    print("FAIL: " + msg[:200]); sys.exit(1)

if __name__ == "__main__":
    main()
