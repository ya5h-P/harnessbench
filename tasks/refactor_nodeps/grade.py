import sys, os, subprocess, glob
PROBE = 'import report\nassert report.generate("Ada", 3) == "Hello Ada, you have 3 messages.", report.generate("Ada", 3)\nassert report.generate("Bo", 0) == "Hello Bo, you have 0 messages."\nprint("BEHAVIOR OK")\n'

def main():
    w = sys.argv[1]
    # constraint 1: the vendored dependency must be gone and unreferenced
    if os.path.exists(os.path.join(w, "tinytemplate.py")):
        print("FAIL: tinytemplate.py still present (the vendored dep must be removed)"); sys.exit(1)
    for f in glob.glob(os.path.join(w, "**", "*.py"), recursive=True):
        if "tinytemplate" in open(f, encoding="utf-8").read():
            print("FAIL: a .py file still references tinytemplate"); sys.exit(1)
    # constraint 2: the required migration_notes.md artifact exists and is non-trivial
    notes = os.path.join(w, "migration_notes.md")
    if not os.path.exists(notes):
        print("FAIL: migration_notes.md not written (required deliverable)"); sys.exit(1)
    txt = open(notes, encoding="utf-8").read()
    if len(txt.strip()) < 40 or "tinytemplate" not in txt:
        print("FAIL: migration_notes.md must describe removing tinytemplate"); sys.exit(1)
    # behavior preserved
    r = subprocess.run([sys.executable, "-c", PROBE], cwd=w, capture_output=True, text=True, timeout=60)
    if "BEHAVIOR OK" not in r.stdout or r.returncode != 0:
        msg = (r.stderr.strip().splitlines() or [r.stdout.strip() or "?"])[-1]
        print("FAIL: " + msg[:200]); sys.exit(1)
    print("REFACTOR_NODEPS OK")

if __name__ == "__main__":
    main()
