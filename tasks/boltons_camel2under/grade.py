import sys, os, importlib.util
def load(wd,n):
    s=importlib.util.spec_from_file_location(n,os.path.join(wd,n+'.py')); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def main():
    wd=sys.argv[1]
    if not os.path.exists(os.path.join(wd,"strutils.py")): print("FAIL: strutils.py missing"); sys.exit(1)
    try: f=load(wd,"strutils").camel2under
    except Exception as e: print("FAIL: import %r"%e); sys.exit(1)
    exp={"BasicParseTest":"basic_parse_test","HTMLParser":"html_parser","Foo":"foo","already_under":"already_under"}
    for s,e in exp.items():
        if f(s)!=e: print("FAIL: camel2under(%r)=%r exp %r"%(s,f(s),e)); sys.exit(1)
    print("CAMEL OK")
main()
