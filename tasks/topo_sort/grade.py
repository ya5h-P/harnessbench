import sys, os, importlib.util
def load(wd,n):
    s=importlib.util.spec_from_file_location(n,os.path.join(wd,n+".py")); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
def valid(graph, order):
    if sorted(map(str,order))!=sorted(map(str,graph.keys())): return False
    pos={k:i for i,k in enumerate(order)}
    if len(pos)!=len(order): return False
    for node, prereqs in graph.items():
        for p in prereqs:
            if pos[p] >= pos[node]: return False
    return True
def main():
    wd=sys.argv[1]
    if not os.path.exists(os.path.join(wd,"topo.py")): print("FAIL: topo.py missing"); sys.exit(1)
    try: topo_sort=load(wd,"topo").topo_sort
    except Exception as e: print("FAIL: import %r"%e); sys.exit(1)
    dags=[{"a":[],"b":["a"],"c":["a"],"d":["b","c"]},{1:[],2:[1],3:[2],4:[3]},
          {"x":[],"y":[],"z":["x","y"],"w":["z"]},{"only":[]}]
    try:
        for g in dags:
            o=topo_sort(g)
            if not valid(g,o): print("FAIL: invalid order %r for %r"%(o,g)); sys.exit(1)
        for cyc in [{"a":["b"],"b":["a"]},{1:[3],2:[1],3:[2]}]:
            try:
                topo_sort(cyc); print("FAIL: cycle not detected"); sys.exit(1)
            except ValueError: pass
    except SystemExit: raise
    except Exception as e:
        print("FAIL: error %r"%e); sys.exit(1)
    print("TOPO OK")
main()
