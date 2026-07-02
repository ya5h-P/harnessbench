import json, sys
src, dst = sys.argv[1], sys.argv[2]
data = json.load(open(src))
json.dump([r for r in data if r.get("ok")], open(dst, "w"))
