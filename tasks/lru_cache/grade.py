import sys, os, importlib.util
def load(wd,n):
    s=importlib.util.spec_from_file_location(n,os.path.join(wd,n+".py")); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
def main():
    wd=sys.argv[1]
    if not os.path.exists(os.path.join(wd,"lru.py")): print("FAIL: lru.py missing"); sys.exit(1)
    try: LRU=load(wd,"lru").LRU
    except Exception as e: print("FAIL: import %r"%e); sys.exit(1)
    try:
        c=LRU(2)
        c.put(1,1); c.put(2,2)
        assert c.get(1)==1            # 1 now MRU
        c.put(3,3)                    # evicts 2 (LRU)
        assert c.get(2) is None, "2 should be evicted"
        c.put(4,4)                    # evicts 1
        assert c.get(1) is None, "1 should be evicted"
        assert c.get(3)==3 and c.get(4)==4
        # update marks recency
        c2=LRU(2); c2.put("a",1); c2.put("b",2); c2.put("a",10)  # a refreshed
        c2.put("c",3)                 # evicts b
        assert c2.get("b") is None and c2.get("a")==10 and c2.get("c")==3
        # capacity 1
        c3=LRU(1); c3.put(1,1); c3.put(2,2); assert c3.get(1) is None and c3.get(2)==2
        assert c.get(99) is None
    except AssertionError as e:
        print("FAIL: %s"%e); sys.exit(1)
    except Exception as e:
        print("FAIL: error %r"%e); sys.exit(1)
    print("LRU OK")
main()
