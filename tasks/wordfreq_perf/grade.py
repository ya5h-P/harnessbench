import sys, os, importlib.util
def load(wd,n):
    s=importlib.util.spec_from_file_location(n,os.path.join(wd,n+'.py')); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

import time, random
def naive(words,k):
    uniq=[]
    for w in words:
        if w not in uniq: uniq.append(w)
    c=[(w,words.count(w)) for w in uniq]; c.sort(key=lambda p:(-p[1],p[0])); return c[:k]
def main():
    wd=sys.argv[1]
    if not os.path.exists(os.path.join(wd,"wordfreq.py")): print("FAIL: wordfreq.py missing"); sys.exit(1)
    try: tw=load(wd,"wordfreq").top_words
    except Exception as e: print("FAIL: import %r"%e); sys.exit(1)
    random.seed(11)
    for words in [["a","b","a","c","a","b"],[],["z"]*5+["y"]*3+["x"], [random.choice("abcdefgh") for _ in range(200)]]:
        if tw(list(words),3)!=naive(list(words),3): print("FAIL: wrong result on small case"); sys.exit(1)
    big=[str(random.randint(0,4000)) for _ in range(6000)]  # many unique -> naive slow
    t0=time.perf_counter(); rn=naive(big,10); tn=time.perf_counter()-t0
    t0=time.perf_counter(); rf=tw(list(big),10); tf=time.perf_counter()-t0
    if rf!=rn: print("FAIL: wrong result on large input"); sys.exit(1)
    if tn<0.10:
        big=[str(random.randint(0,20000)) for _ in range(14000)]
        t0=time.perf_counter(); naive(big,10); tn=time.perf_counter()-t0
        t0=time.perf_counter(); tw(list(big),10); tf=time.perf_counter()-t0
    sp=tn/max(tf,1e-6)
    if sp<4.0: print("FAIL: not fast enough (%.1fx, need >=4x)"%sp); sys.exit(1)
    print("WORDFREQ OK (%.1fx)"%sp)
main()
