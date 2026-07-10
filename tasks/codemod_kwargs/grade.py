import sys, os, subprocess
PROBE = 'import boxlib, layout, grid, canvas\n# keyword-only enforced: positional call must now be rejected\ntry:\n    boxlib.make_box(1, 2, 3, 4)\n    raise SystemExit("make_box still accepts positional args (not keyword-only)")\nexcept TypeError:\n    pass\n# behavior preserved through the callers\nassert layout.run() == 12, layout.run()\nassert grid.run() == 11, grid.run()\nassert canvas.run() == [{"x":1,"y":1,"w":2,"h":2,"area":4}, {"x":3,"y":3,"w":4,"h":4,"area":16}], canvas.run()\nprint("BEHAVIOR OK")\n'

def main():
    w = sys.argv[1]
    r = subprocess.run([sys.executable, "-c", PROBE], cwd=w, capture_output=True, text=True, timeout=60)
    if "BEHAVIOR OK" not in r.stdout or r.returncode != 0:
        msg = (r.stderr.strip().splitlines() or [r.stdout.strip() or "?"])[-1]
        print("FAIL: " + msg[:200]); sys.exit(1)
    print("CODEMOD_KWARGS OK")

if __name__ == "__main__":
    main()
