import sys, os, re
wd=sys.argv[1]
text=open(os.path.join(wd,"messy.txt"),encoding="utf-8").read()
pat=re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
found=set()
for m in pat.findall(text):
    found.add(m.lower())
open(os.path.join(wd,"emails.txt"),"w",encoding="utf-8").write("\n".join(sorted(found))+"\n")
