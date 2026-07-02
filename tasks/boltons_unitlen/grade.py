import sys, os, importlib.util
def load(wd,n):
    s=importlib.util.spec_from_file_location(n,os.path.join(wd,n+'.py')); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def main():
    wd=sys.argv[1]
    if not os.path.exists(os.path.join(wd,"strutils.py")): print("FAIL: strutils.py missing"); sys.exit(1)
    try: m=load(wd,"strutils"); f=m.unit_len; card=m.cardinalize
    except Exception as e: print("FAIL: import %r"%e); sys.exit(1)
    def ref(it,noun="item"):
        c=len(it); u=card(noun,c); return ("%d %s"%(c,u)) if c else ("No %s"%u)
    for it,noun in [(range(10),"number"),("aeiou","vowel"),([],"worry"),([1],"item"),(range(3),"dog"),("","x")]:
        g=f(it,noun) if noun!="item" else f(it)
        e=ref(it,noun)
        if g!=e: print("FAIL: unit_len(%r,%r)=%r exp %r"%(list(it) if not isinstance(it,str) else it,noun,g,e)); sys.exit(1)
    print("UNITLEN OK")
main()
