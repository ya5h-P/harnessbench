#!/usr/bin/env python3
"""Generate the v2 refactor-under-constraints tasks (2 d4 + 1 d5 stateful).

Each ships a fixture project and a reference refactor. Graders check (a) behavior is
preserved (hidden run in a subprocess) AND (b) the structural constraint the task imposes
(public API frozen, keyword-only signature enforced, vendored dep removed, per-file line
cap, required artifact present). Fixture provably FAILS the constraint; ref PASSES.

Run once:  python tasks/_authoring/gen_refactor.py
Verify:    bash engine/preflight.sh refactor_api_freeze  (etc.)
"""
import json, os, shutil

TASKS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OWNED = []

def emit(tid, diff, timeout, prompt, files, capability, tier="variance", stateful=False, notes=""):
    d = os.path.join(TASKS, tid)
    shutil.rmtree(d, ignore_errors=True)
    meta = {"id": tid, "domain": "refactor-under-constraints", "difficulty": diff,
            "timeout_s": timeout, "reseed": False, "grader_token": tid.upper() + " OK",
            "capability": capability, "tier": tier, "stateful": stateful,
            "notes": notes or "hand-authored v2 refactor task"}
    files = dict(files)
    files["task.json"] = json.dumps(meta, indent=2)
    files["prompt.txt"] = prompt.strip() + "\n"
    for rel, content in files.items():
        p = os.path.join(d, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8", newline="\n").write(content)
    OWNED.append((tid, diff, tier))


# ============================================================ refactor_api_freeze (d4)
def api_freeze():
    # a "god module": one flat file well over the line cap, several public functions +
    # a public entry point describe(). The refactor must split it into a package whose
    # public API is unchanged, with NO single .py file over the cap.
    god = '''"""geometry toolkit — everything in one file (needs splitting)."""
import math

PI = 3.141592653589793


def area_circle(r):
    """Area of a circle of radius r."""
    return PI * r * r


def perimeter_circle(r):
    """Circumference of a circle of radius r."""
    return 2 * PI * r


def area_square(s):
    """Area of a square of side s."""
    return s * s


def perimeter_square(s):
    """Perimeter of a square of side s."""
    return 4 * s


def area_rect(w, h):
    """Area of a w x h rectangle."""
    return w * h


def perimeter_rect(w, h):
    """Perimeter of a w x h rectangle."""
    return 2 * (w + h)


def area_triangle(b, h):
    """Area of a triangle with base b and height h."""
    return 0.5 * b * h


def hypotenuse(a, b):
    """Hypotenuse of a right triangle with legs a and b."""
    return math.sqrt(a * a + b * b)


def describe(shape, *dims):
    """Return "<shape>: area=<a>, perimeter=<p>" for shape in
    {circle, square, rect, triangle}. Triangle reports perimeter as the sum of the
    two given legs plus the hypotenuse (a right triangle b, h)."""
    if shape == "circle":
        return "circle: area=%.4f, perimeter=%.4f" % (area_circle(dims[0]), perimeter_circle(dims[0]))
    if shape == "square":
        return "square: area=%.4f, perimeter=%.4f" % (area_square(dims[0]), perimeter_square(dims[0]))
    if shape == "rect":
        return "rect: area=%.4f, perimeter=%.4f" % (area_rect(dims[0], dims[1]),
                                                    perimeter_rect(dims[0], dims[1]))
    if shape == "triangle":
        b, h = dims[0], dims[1]
        peri = b + h + hypotenuse(b, h)
        return "triangle: area=%.4f, perimeter=%.4f" % (area_triangle(b, h), peri)
    raise ValueError("unknown shape: %s" % shape)
'''
    # reference package: __init__ re-exports the frozen public API from small submodules,
    # every file under the 40-line cap.
    ref_init = '''"""geometry package — public API re-exported from submodules."""
from .circle import area_circle, perimeter_circle
from .square import area_square, perimeter_square
from .rect import area_rect, perimeter_rect
from .triangle import area_triangle, hypotenuse
from .describe import describe

PI = 3.141592653589793

__all__ = ["PI", "area_circle", "perimeter_circle", "area_square", "perimeter_square",
           "area_rect", "perimeter_rect", "area_triangle", "hypotenuse", "describe"]
'''
    ref_circle = '''PI = 3.141592653589793


def area_circle(r):
    """Area of a circle of radius r."""
    return PI * r * r


def perimeter_circle(r):
    """Circumference of a circle of radius r."""
    return 2 * PI * r
'''
    ref_square = '''def area_square(s):
    """Area of a square of side s."""
    return s * s


def perimeter_square(s):
    """Perimeter of a square of side s."""
    return 4 * s
'''
    ref_rect = '''def area_rect(w, h):
    """Area of a w x h rectangle."""
    return w * h


def perimeter_rect(w, h):
    """Perimeter of a w x h rectangle."""
    return 2 * (w + h)
'''
    ref_triangle = '''import math


def area_triangle(b, h):
    """Area of a triangle with base b and height h."""
    return 0.5 * b * h


def hypotenuse(a, b):
    """Hypotenuse of a right triangle with legs a and b."""
    return math.sqrt(a * a + b * b)
'''
    ref_describe = '''from .circle import area_circle, perimeter_circle
from .square import area_square, perimeter_square
from .rect import area_rect, perimeter_rect
from .triangle import area_triangle, hypotenuse


def describe(shape, *dims):
    """Return "<shape>: area=<a>, perimeter=<p>" for the supported shapes."""
    if shape == "circle":
        return "circle: area=%.4f, perimeter=%.4f" % (area_circle(dims[0]), perimeter_circle(dims[0]))
    if shape == "square":
        return "square: area=%.4f, perimeter=%.4f" % (area_square(dims[0]), perimeter_square(dims[0]))
    if shape == "rect":
        return "rect: area=%.4f, perimeter=%.4f" % (area_rect(dims[0], dims[1]),
                                                    perimeter_rect(dims[0], dims[1]))
    if shape == "triangle":
        b, h = dims[0], dims[1]
        peri = b + h + hypotenuse(b, h)
        return "triangle: area=%.4f, perimeter=%.4f" % (area_triangle(b, h), peri)
    raise ValueError("unknown shape: %s" % shape)
'''
    probe = r'''import geometry
# frozen public API: names importable at top level and behavior identical
assert abs(geometry.area_circle(2) - 12.566370614) < 1e-6
assert abs(geometry.perimeter_square(3) - 12) < 1e-9
assert geometry.area_rect(3, 4) == 12
assert geometry.describe("circle", 2) == "circle: area=12.5664, perimeter=12.5664"
assert geometry.describe("rect", 3, 4) == "rect: area=12.0000, perimeter=14.0000"
assert geometry.describe("triangle", 3, 4) == "triangle: area=6.0000, perimeter=12.0000"
from geometry import describe, area_circle, hypotenuse
assert hypotenuse(3, 4) == 5
print("BEHAVIOR OK")
'''
    grade = ('import sys, os, subprocess, glob\nPROBE = %r\nCAP = 40\n' % probe) + r'''
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
'''
    # reference solver (run by preflight): builds the package and deletes the god module.
    pkg = {"__init__.py": ref_init, "circle.py": ref_circle, "square.py": ref_square,
           "rect.py": ref_rect, "triangle.py": ref_triangle, "describe.py": ref_describe}
    solve = ("import os, sys\nw = sys.argv[1]\nPKG = %r\n"
             "os.makedirs(os.path.join(w, 'geometry'), exist_ok=True)\n"
             "for name, src in PKG.items():\n"
             "    open(os.path.join(w, 'geometry', name), 'w', encoding='utf-8').write(src)\n"
             "os.remove(os.path.join(w, 'geometry.py'))\n" % pkg)
    emit("refactor_api_freeze", 4, 600,
         "geometry.py is a single 'god module' (well over 40 lines) exposing a public API: the "
         "area_*/perimeter_* helpers, hypotenuse, PI, and describe(shape, *dims). Refactor it into a "
         "geometry/ PACKAGE so that no single .py file exceeds 40 lines, WITHOUT changing the public "
         "API or any behavior: `import geometry` and `from geometry import describe, area_circle, ...` "
         "must keep working with identical results, and the flat geometry.py must no longer exist. "
         "Verify by running python.",
         {"fixtures/geometry.py": god, "ref/solve.py": solve, "grade.py": grade},
         capability="structural-refactor", tier="variance",
         notes="split god-module into a package under a per-file line cap, public API frozen")


# ============================================================ codemod_kwargs (d4)
def codemod_kwargs():
    lib = '''def make_box(x, y, w, h):
    """Return a box dict. NOTE: being migrated to keyword-only arguments."""
    return {"x": x, "y": y, "w": w, "h": h, "area": w * h}
'''
    lib_ref = '''def make_box(*, x, y, w, h):
    """Return a box dict. Arguments are keyword-only."""
    return {"x": x, "y": y, "w": w, "h": h, "area": w * h}
'''
    callers = {
        "layout.py": ('from boxlib import make_box\n\n'
                      'def run():\n    return make_box(%s)["area"]\n'),
        "grid.py": ('import boxlib\n\n'
                    'def run():\n    b = boxlib.make_box(%s)\n    return b["w"] + b["h"]\n'),
        "canvas.py": ('from boxlib import make_box\n\n'
                      'def run():\n    return [make_box(%s), make_box(%s)]\n'),
    }
    # fixture: positional calls; ref: keyword calls
    fx = {
        "layout.py": callers["layout.py"] % "1, 2, 3, 4",
        "grid.py": callers["grid.py"] % "0, 0, 5, 6",
        "canvas.py": callers["canvas.py"] % ("1, 1, 2, 2", "3, 3, 4, 4"),
    }
    rf = {
        "layout.py": callers["layout.py"] % "x=1, y=2, w=3, h=4",
        "grid.py": callers["grid.py"] % "x=0, y=0, w=5, h=6",
        "canvas.py": callers["canvas.py"] % ("x=1, y=1, w=2, h=2", "x=3, y=3, w=4, h=4"),
    }
    probe = r'''import boxlib, layout, grid, canvas
# keyword-only enforced: positional call must now be rejected
try:
    boxlib.make_box(1, 2, 3, 4)
    raise SystemExit("make_box still accepts positional args (not keyword-only)")
except TypeError:
    pass
# behavior preserved through the callers
assert layout.run() == 12, layout.run()
assert grid.run() == 11, grid.run()
assert canvas.run() == [{"x":1,"y":1,"w":2,"h":2,"area":4}, {"x":3,"y":3,"w":4,"h":4,"area":16}], canvas.run()
print("BEHAVIOR OK")
'''
    grade = ('import sys, os, subprocess\nPROBE = %r\n' % probe) + r'''
def main():
    w = sys.argv[1]
    r = subprocess.run([sys.executable, "-c", PROBE], cwd=w, capture_output=True, text=True, timeout=60)
    if "BEHAVIOR OK" not in r.stdout or r.returncode != 0:
        msg = (r.stderr.strip().splitlines() or [r.stdout.strip() or "?"])[-1]
        print("FAIL: " + msg[:200]); sys.exit(1)
    print("CODEMOD_KWARGS OK")

if __name__ == "__main__":
    main()
'''
    files = {"fixtures/boxlib.py": lib, "ref/boxlib.py": lib_ref, "grade.py": grade}
    for name, src in fx.items():
        files["fixtures/" + name] = src
    for name, src in rf.items():
        files["ref/" + name] = src
    emit("codemod_kwargs", 4, 540,
         "boxlib.make_box(x, y, w, h) is being migrated to KEYWORD-ONLY arguments. Change its "
         "signature to keyword-only (def make_box(*, x, y, w, h)) and update EVERY call site across "
         "the project (layout.py, grid.py, canvas.py) to pass arguments by keyword. After your change "
         "a positional call make_box(1, 2, 3, 4) must raise TypeError, and every module's run() must "
         "return exactly what it did before. Verify by running python.",
         files, capability="cross-file-consistency", tier="variance",
         notes="signature migration to keyword-only across all callers")


# ============================================================ refactor_nodeps (d5, stateful)
def nodeps():
    vendored = '''"""tinytemplate — a tiny vendored templating helper (to be removed)."""

def render(template, context):
    """Replace each {key} in template with str(context[key])."""
    out = template
    for k, v in context.items():
        out = out.replace("{" + k + "}", str(v))
    return out
'''
    app = '''import tinytemplate

GREETING = "Hello {name}, you have {count} messages."


def generate(name, count):
    """Render the greeting for a user."""
    return tinytemplate.render(GREETING, {"name": name, "count": count})
'''
    app_ref = '''GREETING = "Hello {name}, you have {count} messages."


def generate(name, count):
    """Render the greeting for a user (now using the stdlib str.format)."""
    return GREETING.format(name=name, count=count)
'''
    notes_ref = '''# Migration notes

Removed the vendored `tinytemplate` module and replaced its `render()` with the standard
library. `report.generate()` now uses `str.format` on the `{name}`/`{count}` placeholders,
producing byte-identical output. `tinytemplate.py` has been deleted and is no longer imported.
'''
    probe = r'''import report
assert report.generate("Ada", 3) == "Hello Ada, you have 3 messages.", report.generate("Ada", 3)
assert report.generate("Bo", 0) == "Hello Bo, you have 0 messages."
print("BEHAVIOR OK")
'''
    grade = ('import sys, os, subprocess, glob\nPROBE = %r\n' % probe) + r'''
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
'''
    emit("refactor_nodeps", 5, 600,
         "report.py depends on a vendored module tinytemplate.py for its {placeholder} rendering. "
         "Remove that dependency: reimplement report.generate() using only the Python standard "
         "library (its output must stay byte-identical), delete tinytemplate.py, and ensure no file "
         "imports it anymore. FIRST write a short migration_notes.md at the project root describing "
         "what you removed and what replaced it (it must mention tinytemplate), THEN make the code "
         "change consistent with those notes. Verify by running python.",
         {"fixtures/tinytemplate.py": vendored, "fixtures/report.py": app,
          "ref/solve.py": ("import os, sys\nw = sys.argv[1]\n"
                           "open(os.path.join(w, 'report.py'), 'w', encoding='utf-8').write(%r)\n"
                           "open(os.path.join(w, 'migration_notes.md'), 'w', encoding='utf-8').write(%r)\n"
                           "os.remove(os.path.join(w, 'tinytemplate.py'))\n" % (app_ref, notes_ref)),
          "grade.py": grade},
         capability="dependency-removal", tier="systematic", stateful=True,
         notes="remove vendored dep -> stdlib; requires a migration_notes.md artifact (stateful)")


def main():
    api_freeze(); codemod_kwargs(); nodeps()
    tally = {}
    for _, d, _ in OWNED:
        tally[d] = tally.get(d, 0) + 1
    print("authored %d refactor tasks; difficulty tally: %s" % (len(OWNED), dict(sorted(tally.items()))))

if __name__ == "__main__":
    main()
