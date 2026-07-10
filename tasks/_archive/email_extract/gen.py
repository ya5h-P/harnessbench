import sys, os, random
workdir, gradedir, seed = sys.argv[1], sys.argv[2], int(sys.argv[3])
random.seed(seed)
names=["alice","bob.smith","carol_3","dev-team","x.y","jane99","m+tag"]
doms=["example.com","mail.co.uk","foo-bar.org","a.io","test.net"]
emails=set()
words=[]
for _ in range(random.randint(8,16)):
    e="%s@%s"%(random.choice(names),random.choice(doms)); emails.add(e.lower()); words.append("contact "+e)
# decoys that must NOT match
for d in ["not@an","bad@domain","@nope.com","plain.text","a@@b.com","x@y.c"]:
    words.append("noise "+d)
for _ in range(20): words.append(random.choice(["lorem","ipsum","dolor","sit-amet","42","---"]))
random.shuffle(words)
open(os.path.join(workdir,"messy.txt"),"w",encoding="utf-8").write("  ".join(words)+"\n")
open(os.path.join(gradedir,"expected.txt"),"w",encoding="utf-8").write("\n".join(sorted(emails))+"\n")
