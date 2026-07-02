import sys, os, importlib.util
def load(wd,n):
    s=importlib.util.spec_from_file_location(n,os.path.join(wd,n+'.py')); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def main():
    wd=sys.argv[1]
    if not os.path.exists(os.path.join(wd,"littleutils.py")): print("FAIL: littleutils.py missing"); sys.exit(1)
    try: g=load(wd,"littleutils").group_by_key_func
    except Exception as e: print("FAIL: import %r"%e); sys.exit(1)
    try:
        r=g("a bb ccc d ee fff".split(), len)
        assert dict(r)=={1:['a','d'],2:['bb','ee'],3:['ccc','fff']}, dict(r)
        r2=g([-1,0,1,3,6,8,9,2], lambda x:x%2)
        assert dict(r2)=={0:[0,6,8,2],1:[-1,1,3,9]}, dict(r2)
        assert dict(g([], lambda x:x))=={}
        assert dict(g([5], lambda x:x))=={5:[5]}
        assert dict(g("aa a aaa a".split(), len))=={1:['a','a'],2:['aa'],3:['aaa']}
    except AssertionError as e:
        print("FAIL: %s"%e); sys.exit(1)
    except SystemExit: raise
    except Exception as e:
        print("FAIL: error %r"%e); sys.exit(1)
    print("GROUPBY OK")
main()
