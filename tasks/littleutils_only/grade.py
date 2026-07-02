import sys, os, importlib.util
def load(wd,n):
    s=importlib.util.spec_from_file_location(n,os.path.join(wd,n+'.py')); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def main():
    wd=sys.argv[1]
    if not os.path.exists(os.path.join(wd,"littleutils.py")): print("FAIL: littleutils.py missing"); sys.exit(1)
    try: only=load(wd,"littleutils").only
    except Exception as e: print("FAIL: import %r"%e); sys.exit(1)
    from itertools import repeat
    try:
        assert only([7])==7
        assert only(["x"])=="x"
        assert only((5,))==5
        for bad in [[], [1,2], [1,2,3], list("abc")]:
            try:
                only(bad); print("FAIL: only(%r) should raise"%(bad,)); sys.exit(1)
            except AssertionError: pass
        try:
            only(repeat(5)); print("FAIL: infinite iterable should raise"); sys.exit(1)
        except AssertionError: pass
        assert only(iter([9]))==9   # non-sized single
    except AssertionError as e:
        print("FAIL: %s"%e); sys.exit(1)
    except SystemExit: raise
    except Exception as e:
        print("FAIL: error %r"%e); sys.exit(1)
    print("ONLY OK")
main()
