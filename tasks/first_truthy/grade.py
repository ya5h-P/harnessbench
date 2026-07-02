import sys, os, importlib.util
def load(wd,n):
    s=importlib.util.spec_from_file_location(n,os.path.join(wd,n+'.py')); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def main():
    wd=sys.argv[1]
    if not os.path.exists(os.path.join(wd,"first.py")): print("FAIL: first.py missing"); sys.exit(1)
    try: first=load(wd,"first").first
    except Exception as e: print("FAIL: import %r"%e); sys.exit(1)
    try:
        assert first([0,False,None,[],(),42])==42, "should skip falsy values"
        assert first([0,False,None,[],()]) is None, "all falsy -> None"
        assert first([0,False,None],default="ohai")=="ohai"
        assert first([])is None
        assert first([1,1,3,4,5],key=lambda x:x%2==0)==4
        assert first([2,3],key=lambda x:x>5,default=-1)==-1
        assert first(["","hi","yo"])=="hi"
    except AssertionError as e:
        print("FAIL: %s"%e); sys.exit(1)
    except SystemExit: raise
    except Exception as e:
        print("FAIL: error %r"%e); sys.exit(1)
    print("FIRST OK")
main()
