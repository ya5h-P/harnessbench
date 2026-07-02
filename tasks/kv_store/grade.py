import sys, os, subprocess

HIDDEN = r'''
import os
from kvstore import KV
p = "kv_data.json"
if os.path.exists(p): os.remove(p)
k = KV(p)
k.set("a", 1); k.set("b", [1, 2, {"x": 3}]); k.set("u", " é 中")
assert k.get("a") == 1
# new instance must see persisted data
k2 = KV(p)
assert k2.get("a") == 1, "scalar not persisted"
assert k2.get("b") == [1, 2, {"x": 3}], "nested not persisted"
assert k2.get("u") == " é 中", "unicode not persisted"
assert k2.get("missing") is None
assert k2.get("missing", "d") == "d"
k2.set("a", 99)                      # overwrite persists
k2.delete("b")
k3 = KV(p)
assert k3.get("a") == 99, "overwrite not persisted"
assert k3.get("b") is None, "delete not persisted"
assert set(k3.keys()) == {"a", "u"}, "keys() wrong: %r" % sorted(k3.keys())
print("KV OK")
'''

def main():
    workdir = sys.argv[1]
    if not os.path.exists(os.path.join(workdir, "kvstore.py")):
        print("FAIL: kvstore.py missing"); sys.exit(1)
    r = subprocess.run([sys.executable, "-c", HIDDEN], cwd=workdir,
                       capture_output=True, text=True, timeout=60)
    if "KV OK" in r.stdout and r.returncode == 0:
        print("KV OK"); sys.exit(0)
    print("FAIL: " + (r.stderr.strip().splitlines()[-1] if r.stderr.strip() else r.stdout.strip())[:300])
    sys.exit(1)

if __name__ == "__main__":
    main()
