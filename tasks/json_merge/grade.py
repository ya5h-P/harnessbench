import sys, os, importlib.util, copy
def load(wd,n):
    s=importlib.util.spec_from_file_location(n,os.path.join(wd,n+".py")); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
def main():
    wd=sys.argv[1]
    if not os.path.exists(os.path.join(wd,"merge.py")): print("FAIL: merge.py missing"); sys.exit(1)
    try: dm=load(wd,"merge").deep_merge
    except Exception as e: print("FAIL: import %r"%e); sys.exit(1)
    try:
        a={"x":1,"d":{"p":1,"q":2},"l":[1,2],"keep":9}
        b={"x":2,"d":{"q":3,"r":4},"l":[3],"new":7}
        a0=copy.deepcopy(a); b0=copy.deepcopy(b)
        got=dm(a,b)
        exp={"x":2,"d":{"p":1,"q":3,"r":4},"l":[1,2,3],"keep":9,"new":7}
        assert got==exp, "merge wrong: %r"%got
        assert a==a0 and b==b0, "inputs were mutated"
        assert dm({"k":{"a":1}},{"k":[1]})=={"k":[1]}, "dict vs list override"
        assert dm({"k":5},{"k":{"a":1}})=={"k":{"a":1}}, "scalar vs dict override"
        assert dm({},{"a":1})=={"a":1} and dm({"a":1},{})=={"a":1}
    except AssertionError as e:
        print("FAIL: %s"%e); sys.exit(1)
    except Exception as e:
        print("FAIL: error %r"%e); sys.exit(1)
    print("MERGE OK")
main()
