import sys, os, importlib.util
def load(wd,n):
    s=importlib.util.spec_from_file_location(n,os.path.join(wd,n+'.py')); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def main():
    wd=sys.argv[1]
    if not os.path.exists(os.path.join(wd,"dijkstra.py")): print("FAIL: dijkstra.py missing"); sys.exit(1)
    try: sd=load(wd,"dijkstra").shortest_distance
    except Exception as e: print("FAIL: import %r"%e); sys.exit(1)
    g={"a":{"b":1,"c":4},"b":{"c":2,"d":5},"c":{"d":1},"d":{}}
    checks=[(("a","d"),4),(("a","c"),3),(("a","a"),0),(("b","d"),3),(("d","a"),float("inf")),(("a","b"),1)]
    for (s,e),exp in checks:
        got=sd(g,s,e)
        if got!=exp: print("FAIL: shortest_distance(%r,%r)=%r exp %r"%(s,e,got,exp)); sys.exit(1)
    print("DIJKSTRA OK")
main()
