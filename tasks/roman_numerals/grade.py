import sys, os, subprocess

HIDDEN = r'''
from roman import to_roman, from_roman

def expect_err(fn, label):
    try: fn()
    except ValueError: return
    except Exception as e: raise SystemExit("%s: wrong exception %r" % (label, e))
    raise SystemExit("%s: expected ValueError" % label)

cases = {1:"I",4:"IV",9:"IX",40:"XL",58:"LVIII",90:"XC",400:"CD",944:"CMXLIV",
         1994:"MCMXCIV",2024:"MMXXIV",3999:"MMMCMXCIX"}
for n,r in cases.items():
    if to_roman(n)!=r: raise SystemExit("to_roman(%d)=%r exp %r"%(n,to_roman(n),r))
    if from_roman(r)!=n: raise SystemExit("from_roman(%r)=%r exp %d"%(r,from_roman(r),n))
for bad in [0,4000,-1]:
    expect_err(lambda b=bad: to_roman(b), "to_roman(%r)"%bad)
for bad in ["","iv","IIII","VV","IC","ABC","MMMM"]:
    expect_err(lambda b=bad: from_roman(b), "from_roman(%r)"%bad)
for n in [1,2,3,14,49,99,444,888,2748,3888]:
    if from_roman(to_roman(n))!=n: raise SystemExit("roundtrip %d"%n)
print("ROMAN OK")
'''

def main():
    workdir = sys.argv[1]
    if not os.path.exists(os.path.join(workdir, "roman.py")):
        print("FAIL: roman.py missing"); sys.exit(1)
    r = subprocess.run([sys.executable, "-c", HIDDEN], cwd=workdir,
                       capture_output=True, text=True, timeout=60)
    if "ROMAN OK" in r.stdout and r.returncode == 0:
        print("ROMAN OK"); sys.exit(0)
    msg = (r.stderr.strip().splitlines() or [r.stdout.strip() or "?"])[-1]
    print("FAIL: " + msg[:200]); sys.exit(1)

if __name__ == "__main__":
    main()
