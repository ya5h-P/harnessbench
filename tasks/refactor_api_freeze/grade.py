import sys, os, subprocess, glob
PROBE = 'import geometry\n# frozen public API: names importable at top level and behavior identical\nassert abs(geometry.area_circle(2) - 12.566370614) < 1e-6\nassert abs(geometry.perimeter_square(3) - 12) < 1e-9\nassert geometry.area_rect(3, 4) == 12\nassert geometry.describe("circle", 2) == "circle: area=12.5664, perimeter=12.5664"\nassert geometry.describe("rect", 3, 4) == "rect: area=12.0000, perimeter=14.0000"\nassert geometry.describe("triangle", 3, 4) == "triangle: area=6.0000, perimeter=12.0000"\nfrom geometry import describe, area_circle, hypotenuse\nassert hypotenuse(3, 4) == 5\nprint("BEHAVIOR OK")\n'
CAP = 40

def main():
    w = sys.argv[1]
    # constraint 1: the flat god-module must be gone, replaced by a package
    if os.path.exists(os.path.join(w, "geometry.py")):
        print("FAIL: geometry.py still a single module (must become a package)"); sys.exit(1)
    if not os.path.exists(os.path.join(w, "geometry", "__init__.py")):
        print("FAIL: geometry/__init__.py missing (expected a geometry package)"); sys.exit(1)
    # constraint 2: no .py file over the line cap
    for f in glob.glob(os.path.join(w, "**", "*.py"), recursive=True):
        n = sum(1 for _ in open(f, encoding="utf-8"))
        if n > CAP:
            print("FAIL: %s has %d lines (cap is %d)" % (os.path.relpath(f, w), n, CAP)); sys.exit(1)
    # behavior + frozen API
    r = subprocess.run([sys.executable, "-c", PROBE], cwd=w, capture_output=True, text=True, timeout=60)
    if "BEHAVIOR OK" not in r.stdout or r.returncode != 0:
        msg = (r.stderr.strip().splitlines() or [r.stdout.strip() or "?"])[-1]
        print("FAIL: " + msg[:200]); sys.exit(1)
    print("REFACTOR_API_FREEZE OK")

if __name__ == "__main__":
    main()
