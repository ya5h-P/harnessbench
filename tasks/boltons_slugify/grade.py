import sys, os, importlib.util
def load(wd,n):
    s=importlib.util.spec_from_file_location(n,os.path.join(wd,n+'.py')); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def main():
    wd=sys.argv[1]
    if not os.path.exists(os.path.join(wd,"strutils.py")): print("FAIL: strutils.py missing"); sys.exit(1)
    try: s=load(wd,"strutils").slugify
    except Exception as e: print("FAIL: import %r"%e); sys.exit(1)
    try:
        assert s("First post! Hi!!!!~1    ")=="first_post_hi_1", s("First post! Hi!!!!~1    ")
        assert s("Hello World")=="hello_world"
        assert s("Hello World", delim="-")=="hello-world"
        assert s("Hello World", lower=False)=="Hello_World"
    except AssertionError as e:
        print("FAIL: %s"%e); sys.exit(1)
    except Exception as e: print("FAIL: error %r"%e); sys.exit(1)
    print("SLUGIFY OK")
main()
