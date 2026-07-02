import sys, os, importlib.util
def load(wd,n):
    s=importlib.util.spec_from_file_location(n,os.path.join(wd,n+'.py')); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def main():
    wd=sys.argv[1]
    if not os.path.exists(os.path.join(wd,"littleutils.py")): print("FAIL: littleutils.py missing"); sys.exit(1)
    try: f=load(wd,"littleutils").strip_optional_suffix
    except Exception as e: print("FAIL: import %r"%e); sys.exit(1)
    try:
        assert f("abcdef","def")=="abc"
        assert f("abcdef","123")=="abcdef"
        assert f("file.py",".py")=="file"
        assert f("file.py",".txt")=="file.py"
    except AssertionError as e:
        print("FAIL: %s"%e); sys.exit(1)
    except Exception as e: print("FAIL: error %r"%e); sys.exit(1)
    print("OPTSUFFIX OK")
main()
