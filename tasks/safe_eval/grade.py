import sys, os, importlib.util
def load(wd,n):
    s=importlib.util.spec_from_file_location(n,os.path.join(wd,n+".py")); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
def main():
    wd=sys.argv[1]
    if not os.path.exists(os.path.join(wd,"calc.py")): print("FAIL: calc.py missing"); sys.exit(1)
    try: se=load(wd,"calc").safe_eval
    except Exception as e: print("FAIL: import %r"%e); sys.exit(1)
    oks={"2+3*4":14,"(2+3)*4":20,"2**3**2":512,"7//2":3,"7%3":1,"-5+2":-3,"10/4":2.5,"-(3+4)":-7}
    try:
        for ex,val in oks.items():
            g=se(ex)
            if abs(g-val)>1e-9: print("FAIL: safe_eval(%r)=%r exp %r"%(ex,g,val)); sys.exit(1)
        bad=["__import__('os')","os.system('x')","(1).__class__","a+1","print(1)","[].append(1)","lambda:0","1;2"]
        for ex in bad:
            try:
                r=se(ex); print("FAIL: safe_eval(%r) returned %r, expected ValueError"%(ex,r)); sys.exit(1)
            except ValueError: pass
    except SystemExit: raise
    except Exception as e:
        print("FAIL: unexpected error %r"%e); sys.exit(1)
    print("SAFEEVAL OK")
main()
