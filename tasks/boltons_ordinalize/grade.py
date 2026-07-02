import sys, os, importlib.util
def load(wd,n):
    s=importlib.util.spec_from_file_location(n,os.path.join(wd,n+'.py')); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def main():
    wd=sys.argv[1]
    if not os.path.exists(os.path.join(wd,"strutils.py")): print("FAIL: strutils.py missing"); sys.exit(1)
    try: ordinalize=load(wd,"strutils").ordinalize
    except Exception as e: print("FAIL: import %r"%e); sys.exit(1)
    exp={1:"1st",2:"2nd",3:"3rd",4:"4th",5:"5th",10:"10th",11:"11th",12:"12th",13:"13th",
         21:"21st",22:"22nd",23:"23rd",100:"100th",101:"101st",111:"111th",112:"112th",113:"113th",
         1000:"1000th",3694839230:"3694839230th"}
    try:
        for n,e in exp.items():
            g=ordinalize(n)
            if g!=e: print("FAIL: ordinalize(%r)=%r exp %r"%(n,g,e)); sys.exit(1)
        if ordinalize("hi")!="hi": print("FAIL: non-numeric string should pass through"); sys.exit(1)
    except SystemExit: raise
    except Exception as e:
        print("FAIL: error %r"%e); sys.exit(1)
    print("ORDINAL OK")
main()
