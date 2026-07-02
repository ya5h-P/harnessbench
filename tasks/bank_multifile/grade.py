import sys, os, subprocess

# Run the hidden superset as a subprocess inside the workdir so 'bank' imports correctly.
HIDDEN = r'''
from bank.account import Account
from bank.ledger import Ledger

def expect(exc, fn):
    try: fn()
    except exc: return
    except Exception as e: raise AssertionError("wrong exc %r" % e)
    raise AssertionError("expected " + exc.__name__)

a = Account(100)
a.withdraw(100)                       # exact drain allowed
assert a.balance == 0
expect(ValueError, lambda: a.withdraw(1))   # cannot overdraw empty
assert a.balance == 0
expect(ValueError, lambda: a.withdraw(-5))  # non-positive
expect(ValueError, lambda: a.deposit(0))

L = Ledger()
L.open("x", 50); L.open("y", 10)
L.transfer("x", "y", 30)
assert L.accounts["x"].balance == 20 and L.accounts["y"].balance == 40
# atomic: over-limit transfer must raise and leave BOTH balances unchanged
expect(ValueError, lambda: L.transfer("x", "y", 1000))
assert L.accounts["x"].balance == 20, "src changed after failed transfer"
assert L.accounts["y"].balance == 40, "dst changed after failed transfer"
assert L.total() == 60
print("BANK OK")
'''

def main():
    workdir = sys.argv[1]
    r = subprocess.run([sys.executable, "-c", HIDDEN], cwd=workdir,
                       capture_output=True, text=True, timeout=60)
    if "BANK OK" in r.stdout and r.returncode == 0:
        print("BANK OK"); sys.exit(0)
    print("FAIL: " + (r.stderr.strip().splitlines()[-1] if r.stderr.strip() else r.stdout.strip())[:300])
    sys.exit(1)

if __name__ == "__main__":
    main()
