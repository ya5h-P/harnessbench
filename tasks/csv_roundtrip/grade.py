import sys, os, importlib.util, random
def load(wd,n):
    s=importlib.util.spec_from_file_location(n,os.path.join(wd,n+".py")); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
def main():
    wd=sys.argv[1]
    if not os.path.exists(os.path.join(wd,"csvtool.py")): print("FAIL: csvtool.py missing"); sys.exit(1)
    try:
        mod=load(wd,"csvtool"); parse=mod.parse; dump=mod.dump
    except Exception as e: print("FAIL: import %r"%e); sys.exit(1)
    try:
        assert parse("a,b,c")==["a","b","c"], "plain"
        assert parse('a,"b,c",d')==["a","b,c","d"], "quoted comma"
        assert parse('"she said ""hi""",x')==['she said "hi"',"x"], "escaped quotes"
        assert parse("")==[""] , "empty -> single empty field"
        assert dump(["a","b","c"])=="a,b,c", "dump plain"
        assert dump(["a","b,c"])=='a,"b,c"', "dump comma"
        assert dump(['x"y'])=='"x""y"', "dump quote"
        random.seed(3)
        alpha=['a','b',',','"',' ','z','1']
        for _ in range(300):
            row=[''.join(random.choice(alpha) for _ in range(random.randint(0,6))) for _ in range(random.randint(1,4))]
            if parse(dump(row))!=row:
                print("FAIL: roundtrip failed on %r"%row); sys.exit(1)
    except AssertionError as e:
        print("FAIL: %s"%e); sys.exit(1)
    except Exception as e:
        print("FAIL: error %r"%e); sys.exit(1)
    print("CSV OK")
main()
