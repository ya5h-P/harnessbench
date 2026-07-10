import sys, os, importlib.util
def load(wd,n):
    s=importlib.util.spec_from_file_location(n,os.path.join(wd,n+'.py')); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def main():
    wd=sys.argv[1]
    if not os.path.exists(os.path.join(wd,"littleutils.py")): print("FAIL: littleutils.py missing"); sys.exit(1)
    try: f=load(wd,"littleutils").helpful_error_list_get
    except Exception as e: print("FAIL: import %r"%e); sys.exit(1)
    try:
        assert f([1,2,3],1)==2
        assert f([1,2,3],0)==1
        assert f(["a","b"],-1)=="b"
        for lst,i in [([1,2,3],4),([],0),([1],5),([1,2,3],-9)]:
            try:
                f(lst,i); print("FAIL: get(%r,%r) should raise IndexError"%(lst,i)); sys.exit(1)
            except IndexError: pass
    except AssertionError as e:
        print("FAIL: %s"%e); sys.exit(1)
    except SystemExit: raise
    except Exception as e:
        print("FAIL: error %r"%e); sys.exit(1)
    print("LISTGET OK")
main()
