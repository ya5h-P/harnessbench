import sys, os, importlib.util
def load(wd,n):
    s=importlib.util.spec_from_file_location(n,os.path.join(wd,n+'.py')); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def main():
    wd=sys.argv[1]
    if not os.path.exists(os.path.join(wd,"littleutils.py")): print("FAIL: littleutils.py missing"); sys.exit(1)
    try: f=load(wd,"littleutils").strip_required_suffix
    except Exception as e: print("FAIL: import %r"%e); sys.exit(1)
    try:
        assert f("abcdef","def")=="abc", f("abcdef","def")
        assert f("hello.py",".py")=="hello"
        assert f("aXX","XX")=="a"
        assert f("only","only")==""
        assert f("abcdef","f")=="abcde"
        for s,suf in [("abcdef","123"),("abc","xyz"),("","q")]:
            try:
                f(s,suf); print("FAIL: strip_required_suffix(%r,%r) should raise"%(s,suf)); sys.exit(1)
            except AssertionError: pass
    except AssertionError as e:
        print("FAIL: %s"%e); sys.exit(1)
    except SystemExit: raise
    except Exception as e:
        print("FAIL: error %r"%e); sys.exit(1)
    print("STRIP OK")
main()
