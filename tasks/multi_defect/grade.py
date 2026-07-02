import sys, os, importlib.util
def load(wd,n):
    s=importlib.util.spec_from_file_location(n,os.path.join(wd,n+".py")); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
def ref(w,d,express=False):
    cost = 5.0 + 0.5*w + 0.1*d
    if w > 30: cost += 20.0
    if express: cost *= 1.5
    if cost < 10.0: cost = 10.0
    return round(cost,2)
def main():
    wd=sys.argv[1]
    if not os.path.exists(os.path.join(wd,"shipping.py")): print("FAIL: shipping.py missing"); sys.exit(1)
    try: quote=load(wd,"shipping").quote
    except Exception as e: print("FAIL: import %r"%e); sys.exit(1)
    cases=[(10,100,False),(4,50,False),(0,0,False),(1,1,False),(40,100,False),
           (10,100,True),(40,200,True),(31,0,False),(30,0,False),(2,5,True),(50,500,True),(0,10,False)]
    for w,d,ex in cases:
        try: g=quote(w,d,ex) if ex else quote(w,d)
        except Exception as e: print("FAIL: quote(%r,%r,%r) raised %r"%(w,d,ex,e)); sys.exit(1)
        e=ref(w,d,ex)
        if abs(g-e)>1e-9: print("FAIL: quote(%r,%r,express=%r)=%r expected %r"%(w,d,ex,g,e)); sys.exit(1)
    print("SHIP OK")
main()
