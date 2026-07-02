#!/usr/bin/env python3
"""Materialize a task's workdir (agent-visible) and gradedir (hidden).

usage: setup.py <taskdir> <workdir> <gradedir> <seed> [variant]
  variant: ""(real run) | "ref"(apply reference solution) | "buggy"(unsolved state)
Prints nothing on success; non-zero exit on error.
"""
import sys, os, shutil, subprocess, json

def copytree(src, dst):
    if not os.path.isdir(src):
        return
    for root, _, files in os.walk(src):
        rel = os.path.relpath(root, src)
        out = os.path.join(dst, rel) if rel != "." else dst
        os.makedirs(out, exist_ok=True)
        for f in files:
            shutil.copy2(os.path.join(root, f), os.path.join(out, f))

def main():
    taskdir, workdir, gradedir, seed = sys.argv[1:5]
    variant = sys.argv[5] if len(sys.argv) > 5 else ""
    os.makedirs(workdir, exist_ok=True)
    os.makedirs(gradedir, exist_ok=True)
    task = json.load(open(os.path.join(taskdir, "task.json"), encoding="utf-8"))

    # 1. static fixtures (agent-visible), then reseeded extras via gen.py
    copytree(os.path.join(taskdir, "fixtures"), workdir)
    gen = os.path.join(taskdir, "gen.py")
    if task.get("reseed") and os.path.exists(gen):
        r = subprocess.run([sys.executable, gen, workdir, gradedir, str(seed)])
        if r.returncode != 0:
            print("gen.py failed", file=sys.stderr); sys.exit(2)

    # 2. hidden test files -> gradedir only
    copytree(os.path.join(taskdir, "hidden"), gradedir)

    # 3. variant overlay
    if variant == "ref":
        copytree(os.path.join(taskdir, "ref"), workdir)
        # solve.py is a reference *solver* (run by preflight), not a fixture to leave behind
        sp = os.path.join(workdir, "solve.py")
        if os.path.exists(sp) and not os.path.exists(os.path.join(taskdir, "fixtures", "solve.py")):
            os.remove(sp)
    elif variant == "buggy":
        # explicit buggy state if provided; otherwise the untouched fixtures already are "buggy"
        copytree(os.path.join(taskdir, "buggy"), workdir)

if __name__ == "__main__":
    main()
