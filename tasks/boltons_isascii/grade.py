import sys, os, importlib.util
def load(wd,n):
    s=importlib.util.spec_from_file_location(n,os.path.join(wd,n+'.py')); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def main():
    wd=sys.argv[1]
    if not os.path.exists(os.path.join(wd,"strutils.py")): print("FAIL: strutils.py missing"); sys.exit(1)
    try: f=load(wd,"strutils").is_ascii
    except Exception as e: print("FAIL: import %r"%e); sys.exit(1)
    try:
        assert f("Beyonce")==True
        assert f("Beyoncé")==False, "accented should be non-ascii"
        assert f("plain ascii 123")==True
        assert f("")==True
        assert f(b"abc")==True
        assert f(b"\xff")==False
        for bad in [123, None, 4.5, ["a"]]:
            try:
                f(bad); print("FAIL: is_ascii(%r) should raise ValueError"%(bad,)); sys.exit(1)
            except ValueError: pass
    except AssertionError as e:
        print("FAIL: %s"%e); sys.exit(1)
    except SystemExit: raise
    except Exception as e: print("FAIL: error %r"%e); sys.exit(1)
    print("ISASCII OK")
main()
