import sys, os
def main():
    wd,gd=sys.argv[1],sys.argv[2]
    exp=[l.strip() for l in open(os.path.join(gd,"expected.txt"),encoding="utf-8") if l.strip()]
    p=os.path.join(wd,"emails.txt")
    if not os.path.exists(p): print("FAIL: emails.txt missing"); sys.exit(1)
    got=[l.strip().lower() for l in open(p,encoding="utf-8") if l.strip()]
    if got!=sorted(exp):
        print("FAIL: got %r expected %r"%(got, sorted(exp))); sys.exit(1)
    print("EMAIL OK")
main()
