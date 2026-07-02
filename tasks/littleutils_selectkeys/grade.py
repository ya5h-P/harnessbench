import sys, os, importlib.util
def load(wd,n):
    s=importlib.util.spec_from_file_location(n,os.path.join(wd,n+'.py')); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def main():
    wd=sys.argv[1]
    if not os.path.exists(os.path.join(wd,"littleutils.py")): print("FAIL: littleutils.py missing"); sys.exit(1)
    try: sk=load(wd,"littleutils").select_keys
    except Exception as e: print("FAIL: import %r"%e); sys.exit(1)
    d={"a":1,"b":2,"c":3}
    try:
        assert sk(d,"a c")=={"a":1,"c":3}, sk(d,"a c")
        assert sk(d,["a"])=={"a":1}
        assert sk(d,"a b c")=={"a":1,"b":2,"c":3}
        assert sk(d,[])=={}
        for missing in ["a d","z","b x"]:
            try:
                sk(d,missing); print("FAIL: select_keys with missing key %r should raise KeyError"%missing); sys.exit(1)
            except KeyError: pass
        assert d=={"a":1,"b":2,"c":3}, "input dict was mutated"
    except AssertionError as e:
        print("FAIL: %s"%e); sys.exit(1)
    except SystemExit: raise
    except Exception as e:
        print("FAIL: error %r"%e); sys.exit(1)
    print("SELECTKEYS OK")
main()
