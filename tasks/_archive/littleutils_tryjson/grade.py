import sys, os, importlib.util
def load(wd,n):
    s=importlib.util.spec_from_file_location(n,os.path.join(wd,n+'.py')); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def main():
    wd=sys.argv[1]
    if not os.path.exists(os.path.join(wd,"littleutils.py")): print("FAIL: littleutils.py missing"); sys.exit(1)
    try: f=load(wd,"littleutils").try_parse_json
    except Exception as e: print("FAIL: import %r"%e); sys.exit(1)
    try:
        assert f('{"a": 1}')=={"a":1}
        assert f("[1, 2, 3]")==[1,2,3]
        assert f('"hi"')=="hi"
        assert f("null") is None   # valid JSON null
        for bad in ["", "{bad}", "not json", "{'a':1}", "[1,"]:
            try:
                f(bad); print("FAIL: try_parse_json(%r) should raise ValueError"%bad); sys.exit(1)
            except ValueError: pass
    except AssertionError as e:
        print("FAIL: %s"%e); sys.exit(1)
    except SystemExit: raise
    except Exception as e: print("FAIL: error %r"%e); sys.exit(1)
    print("TRYJSON OK")
main()
