import sys, os, importlib.util
def load(wd,n):
    s=importlib.util.spec_from_file_location(n,os.path.join(wd,n+".py")); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
def main():
    wd=sys.argv[1]
    if not os.path.exists(os.path.join(wd,"fizzbuzz.py")): print("FAIL: fizzbuzz.py missing"); sys.exit(1)
    try: fb=load(wd,"fizzbuzz").fizzbuzz
    except Exception as e: print("FAIL: import %r"%e); sys.exit(1)
    def ref(n):
        out=[]
        for i in range(1,n+1):
            if i%15==0: out.append("FizzBuzz")
            elif i%3==0: out.append("Fizz")
            elif i%5==0: out.append("Buzz")
            else: out.append(i)
        return out
    for n in [1,2,5,15,16,30,100]:
        g=fb(n)
        if g!=ref(n): print("FAIL: fizzbuzz(%d) wrong: %r"%(n,g[:20])); sys.exit(1)
    if fb(5)!=[1,2,"Fizz",4,"Buzz"]: print("FAIL: types wrong (ints must be ints)"); sys.exit(1)
    print("FIZZ OK")
main()
