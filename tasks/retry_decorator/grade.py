import sys, os, importlib.util
def load(wd,n):
    s=importlib.util.spec_from_file_location(n,os.path.join(wd,n+'.py')); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def main():
    wd=sys.argv[1]
    if not os.path.exists(os.path.join(wd,"retry.py")): print("FAIL: retry.py missing"); sys.exit(1)
    try: retry=load(wd,"retry").retry
    except Exception as e: print("FAIL: import %r"%e); sys.exit(1)
    try:
        st={"n":0}
        @retry(times=3)
        def flaky():
            st["n"]+=1
            if st["n"]<3: raise ValueError("boom")
            return "ok"
        assert flaky()=="ok", "should succeed on 3rd try"
        assert st["n"]==3, "attempts=%d"%st["n"]
        st2={"n":0}
        @retry(times=2)
        def bad():
            st2["n"]+=1; raise RuntimeError("nope")
        try:
            bad(); print("FAIL: should have raised"); sys.exit(1)
        except RuntimeError: pass
        assert st2["n"]==2, "should attempt exactly 2: %d"%st2["n"]
        st3={"n":0}
        @retry(times=5)
        def good():
            st3["n"]+=1; return 7
        assert good()==7 and st3["n"]==1, "no retry needed"
    except AssertionError as e:
        print("FAIL: %s"%e); sys.exit(1)
    print("RETRY OK")
main()
