import sys, os, importlib.util
def load(wd,n):
    s=importlib.util.spec_from_file_location(n,os.path.join(wd,n+'.py')); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def main():
    wd=sys.argv[1]
    if not os.path.exists(os.path.join(wd,"parens.py")): print("FAIL: parens.py missing"); sys.exit(1)
    try: f=load(wd,"parens").is_balanced
    except Exception as e: print("FAIL: import %r"%e); sys.exit(1)
    cases={"":True,"()":True,"([]{})":True,"(]":False,"([)]":False,"a(b)c[d]":True,"(((":False,"}{":False,"{[()]}":True,"(()":False}
    for s,exp in cases.items():
        if bool(f(s))!=exp: print("FAIL: is_balanced(%r)=%r exp %r"%(s,f(s),exp)); sys.exit(1)
    print("PARENS OK")
main()
