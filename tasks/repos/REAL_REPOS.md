# Real-repo tasks — curation guide

Real-repo tasks run an agent against a *snapshot of an actual messy GitHub project* and grade the
fix objectively. Snapshots are pinned to a commit SHA and vendored here so the benchmark stays
reproducible even if upstream changes or disappears.

## Vendored so far — 4 repos, 21 real-repo tasks (~40% of the suite)
| name | source | SHA | license | tasks |
|------|--------|-----|---------|-------|
| papergen | github.com/ya5h-P/papergen | 4a06659 | MIT | papergen_repeat (d3) |
| littleutils | github.com/alexmojaki/littleutils | 62d9401 | MIT | only, strip, groupby, listget, selectkeys, stripprefix, tryjson, stripoptprefix, stripoptsuffix, groupbykey (10, d3–d4) |
| first | github.com/hynek/first | d185995 | MIT | first_truthy (d3) |
| boltons | github.com/mahmoud/boltons | 979fa9b | BSD-3 | ordinalize, camel2under, under2camel, a10n, cardinalize, splitpunct, unitlen, isascii, slugify (9, d3) |

**How these work:** each real-repo task ships the *real* source file (a single module or the real
repo) with exactly ONE function mutated to introduce a realistic bug; the agent must navigate the
real code and fix it, and the grader tests the documented behaviour (a hidden superset). `ref/` is
the pristine upstream file, so preflight proves the mutation fails and the original passes.

`papergen` also has multiple bugs in `questionmaker.py` (counter logic, off-by-one insert index,
the `qestion` typo) available to seed a d5 multi-defect task.

## Adding a real-repo task (≈30 min each)
1. **Find** a small, low-star, **permissively-licensed (MIT/Apache/BSD)** Python repo with an
   obvious, reproducible defect or an open bug issue. Prefer few/no third-party deps.
2. **Vendor** it pinned:  `bash fetch_repos.sh <name> <git-url> <commit-sha>`
3. **Create the task** `tasks/<id>/`:
   - `task.json` (domain `real-repo-maintenance` or `multi-defect-debug`, difficulty 3–5).
   - `prompt.txt` — the concrete defect/feature to fix.
   - `fixtures/` — copy the buggy file(s) the agent should edit (and any context like README).
   - `grade.py` — HIDDEN grader: copy the produced file(s) into a clean dir, **run the repo**, and
     assert the defect is gone (use a hidden superset of cases; for multi-defect, require ALL fixed).
   - `ref/` — the corrected file(s) (reference solution) so preflight can prove the grader passes.
4. **Validate**: `bash engine/preflight.sh <id>` must show `buggy rc=1, ref rc=0`.

## Vetting checklist (reject if any fails)
- clones + runs on plain Python (pin the interpreter; avoid heavy deps).
- the defect is reproducible and the fix is objectively checkable by executing the code.
- license is permissive; `PROVENANCE.txt` records source + SHA + license.
- the grader cannot be gamed by editing the shown test (grade against a hidden superset / fresh copy).

## Target mix
~40% of the suite should be real-repo tasks (≈13 of ~32), spread across difficulty 3–5, including a
few d5 multi-defect repos. The remaining ~60% are the controlled synthetic tasks, which exist to
cover difficulty bands and domains (perf, concurrency, security, codemod, …) that the available
real repos don't cleanly provide.
