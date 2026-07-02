import sys, os, importlib.util
def load(wd,n):
    s=importlib.util.spec_from_file_location(n,os.path.join(wd,n+'.py')); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def main():
    wd=sys.argv[1]
    if not os.path.exists(os.path.join(wd,"sqlsafe.py")): print("FAIL: sqlsafe.py missing"); sys.exit(1)
    try: bw=load(wd,"sqlsafe").build_where
    except Exception as e: print("FAIL: import %r"%e); sys.exit(1)
    try:
        sql,params=bw({"name":"bob","age":30})
        assert sql=="age = ? AND name = ?", "sql=%r"%sql
        assert params==[30,"bob"], "params=%r"%params
        assert bw({})==("",[]), "empty"
        evil="1 OR 1=1; DROP TABLE users --"
        sql2,params2=bw({"x":evil})
        assert sql2=="x = ?", "sql2=%r"%sql2
        assert params2==[evil], "value must be in params"
        assert evil not in sql2, "INJECTION: value was inlined into sql"
        assert sql2.count("?")==1
        sql3,p3=bw({"b":2,"a":1,"c":3})
        assert sql3=="a = ? AND b = ? AND c = ?" and p3==[1,2,3], "%r %r"%(sql3,p3)
    except AssertionError as e:
        print("FAIL: %s"%e); sys.exit(1)
    print("SQLSAFE OK")
main()
