import sys, os, importlib.util
def load(wd,n):
    s=importlib.util.spec_from_file_location(n,os.path.join(wd,n+'.py')); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

import threading
def main():
    wd=sys.argv[1]
    if not os.path.exists(os.path.join(wd,"idgen.py")): print("FAIL: idgen.py missing"); sys.exit(1)
    try: m=load(wd,"idgen")
    except Exception as e: print("FAIL: import %r"%e); sys.exit(1)
    T,PER,TRIALS=8,200,3; total=T*PER
    for _ in range(TRIALS):
        if hasattr(m,"reset"): m.reset()
        got=[]; lock=threading.Lock()
        def work():
            loc=[m.next_id() for _ in range(PER)]
            with lock: got.extend(loc)
        ts=[threading.Thread(target=work) for _ in range(T)]
        for t in ts: t.start()
        for t in ts: t.join()
        if len(got)!=total or len(set(got))!=total:
            print("FAIL: duplicate ids (%d unique of %d)"%(len(set(got)),total)); sys.exit(1)
        if set(got)!=set(range(total)):
            print("FAIL: ids not exactly 0..N-1"); sys.exit(1)
    print("IDGEN OK")
main()
