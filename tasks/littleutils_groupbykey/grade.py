import sys, os, importlib.util
def load(wd,n):
    s=importlib.util.spec_from_file_location(n,os.path.join(wd,n+'.py')); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def main():
    wd=sys.argv[1]
    if not os.path.exists(os.path.join(wd,"littleutils.py")): print("FAIL: littleutils.py missing"); sys.exit(1)
    try: g=load(wd,"littleutils").group_by_key
    except Exception as e: print("FAIL: import %r"%e); sys.exit(1)
    data=[{"t":"a","v":1},{"t":"b","v":2},{"t":"a","v":3}]
    try:
        r=dict(g(data,"t"))
        assert r=={"a":[data[0],data[2]],"b":[data[1]]}, r
        r2=dict(g([{"k":1},{"k":1},{"k":2}], "k"))
        assert r2=={1:[{"k":1},{"k":1}],2:[{"k":2}]}, r2
        assert dict(g([], "x"))=={}
    except AssertionError as e:
        print("FAIL: %s"%e); sys.exit(1)
    except Exception as e: print("FAIL: error %r"%e); sys.exit(1)
    print("GROUPKEY OK")
main()
