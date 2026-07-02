import sys, os, importlib.util
def load(wd,n):
    s=importlib.util.spec_from_file_location(n,os.path.join(wd,n+'.py')); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def main():
    wd=sys.argv[1]
    if not os.path.exists(os.path.join(wd,"intervals.py")): print("FAIL: intervals.py missing"); sys.exit(1)
    try: merge=load(wd,"intervals").merge
    except Exception as e: print("FAIL: import %r"%e); sys.exit(1)
    cases=[([],[]),([[1,3]],[[1,3]]),([[1,3],[2,6],[8,10],[15,18]],[[1,6],[8,10],[15,18]]),
           ([[1,4],[4,5]],[[1,5]]),([[5,6],[1,3],[2,2]],[[1,3],[5,6]]),([[1,10],[2,3],[4,5]],[[1,10]])]
    for inp,exp in cases:
        src=[list(x) for x in inp]
        got=merge([list(x) for x in inp])
        if [list(x) for x in got]!=exp: print("FAIL: merge(%r)=%r exp %r"%(inp,got,exp)); sys.exit(1)
    print("INTERVAL OK")
main()
