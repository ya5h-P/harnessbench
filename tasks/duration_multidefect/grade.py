import sys, os, importlib.util
def load(wd,n):
    s=importlib.util.spec_from_file_location(n,os.path.join(wd,n+'.py')); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def main():
    wd=sys.argv[1]
    if not os.path.exists(os.path.join(wd,"duration.py")): print("FAIL: duration.py missing"); sys.exit(1)
    try:
        m=load(wd,"duration"); pd=m.parse_duration; fd=m.format_duration
    except Exception as e: print("FAIL: import %r"%e); sys.exit(1)
    parse_cases={"45m":2700,"1h30m15s":5415,"2h":7200,"90s":90,"1h5s":3605,"0s":0}
    fmt_cases={5415:"1h30m15s",2700:"45m",3600:"1h",0:"0s",90:"1m30s",3661:"1h1m1s",59:"59s"}
    try:
        for s,exp in parse_cases.items():
            if pd(s)!=exp: print("FAIL: parse_duration(%r)=%r exp %r"%(s,pd(s),exp)); sys.exit(1)
        for n,exp in fmt_cases.items():
            if fd(n)!=exp: print("FAIL: format_duration(%r)=%r exp %r"%(n,fd(n),exp)); sys.exit(1)
        for n in [0,1,59,60,61,3600,3661,5415,86399,100000]:
            if pd(fd(n))!=n: print("FAIL: roundtrip failed for %d (fmt=%r)"%(n,fd(n))); sys.exit(1)
        for bad in ["","x","h","1x","abc"]:
            try:
                pd(bad); print("FAIL: parse_duration(%r) should raise"%bad); sys.exit(1)
            except ValueError: pass
    except SystemExit: raise
    except Exception as e:
        print("FAIL: error %r"%e); sys.exit(1)
    print("DURATION OK")
main()
