import sys, os, importlib.util
def load(wd,n):
    s=importlib.util.spec_from_file_location(n,os.path.join(wd,n+'.py')); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def main():
    wd=sys.argv[1]
    if not os.path.exists(os.path.join(wd,"strutils.py")): print("FAIL: strutils.py missing"); sys.exit(1)
    try: f=load(wd,"strutils").split_punct_ws
    except Exception as e: print("FAIL: import %r"%e); sys.exit(1)
    cases={"First post! Hi!!!!~1    ":["First","post","Hi","1"],"a,b,,c":["a","b","c"],
           "   ":[],"one":["one"],"x--y  z":["x","y","z"]}
    for s,e in cases.items():
        if f(s)!=e: print("FAIL: split_punct_ws(%r)=%r exp %r"%(s,f(s),e)); sys.exit(1)
    print("SPLITPUNCT OK")
main()
