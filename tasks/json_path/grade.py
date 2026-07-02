import sys, os, importlib.util
def load(wd,n):
    s=importlib.util.spec_from_file_location(n,os.path.join(wd,n+'.py')); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def main():
    wd=sys.argv[1]
    if not os.path.exists(os.path.join(wd,"jsonpath.py")): print("FAIL: jsonpath.py missing"); sys.exit(1)
    try: gp=load(wd,"jsonpath").get_path
    except Exception as e: print("FAIL: import %r"%e); sys.exit(1)
    obj={"a":{"b":[{"c":1},{"c":2}]},"x":5,"list":[10,20,30]}
    checks=[("a.b.0.c",1),("a.b.1.c",2),("x",5),("list.2",30),("a.b.5.c",None),
            ("a.z",None),("x.y",None),("list.9","D"),("nope","D")]
    for path,exp in checks:
        d="D" if exp=="D" else None
        got=gp(obj,path,d)
        want=exp if exp!="D" else "D"
        if got!=want: print("FAIL: get_path(%r)=%r exp %r"%(path,got,want)); sys.exit(1)
    print("JSONPATH OK")
main()
