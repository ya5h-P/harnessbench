import sys, os, importlib.util
def load(wd,n):
    s=importlib.util.spec_from_file_location(n,os.path.join(wd,n+'.py')); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def main():
    wd=sys.argv[1]
    if not os.path.exists(os.path.join(wd,"littleutils.py")): print("FAIL: littleutils.py missing"); sys.exit(1)
    try: f=load(wd,"littleutils").strip_required_prefix
    except Exception as e: print("FAIL: import %r"%e); sys.exit(1)
    try:
        assert f("abcdef","abc")=="def", f("abcdef","abc")
        assert f("hello","he")=="llo"
        assert f("xy","x")=="y"
        assert f("same","same")==""
        for s,p in [("abcdef","123"),("abc","z"),("","q")]:
            try:
                f(s,p); print("FAIL: strip_required_prefix(%r,%r) should raise"%(s,p)); sys.exit(1)
            except AssertionError: pass
    except AssertionError as e:
        print("FAIL: %s"%e); sys.exit(1)
    except SystemExit: raise
    except Exception as e: print("FAIL: error %r"%e); sys.exit(1)
    print("PREFIX OK")
main()
