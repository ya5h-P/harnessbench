import sys, os, importlib.util
def load(wd,n):
    s=importlib.util.spec_from_file_location(n,os.path.join(wd,n+'.py')); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def main():
    wd=sys.argv[1]
    if not os.path.exists(os.path.join(wd,"interp.py")): print("FAIL: interp.py missing"); sys.exit(1)
    try: run=load(wd,"interp").run
    except Exception as e: print("FAIL: import %r"%e); sys.exit(1)
    try:
        assert run("print 2 + 3 * 4")==[14]
        assert run("print (2 + 3) * 4")==[20]
        assert run("print 10 - 2 - 3")==[5]
        assert run("x = 3\ny = x + 4\nprint y\nprint x * y")==[7,21]
        assert run("a = 2 + 3 * 4\nprint a")==[14]
        assert run("print 2 * 3 + 4 * 5")==[26]
        assert run("x = 5\ny = (x - 1) * (x + 1)\nprint y")==[24]
        assert run("print 7")==[7]
        try:
            run("print undefinedvar"); print("FAIL: undefined var should raise"); sys.exit(1)
        except (NameError, KeyError): pass
    except AssertionError as e:
        print("FAIL: wrong result (%s)"%e); sys.exit(1)
    except SystemExit: raise
    except Exception as e:
        print("FAIL: error %r"%e); sys.exit(1)
    print("INTERP OK")
main()
