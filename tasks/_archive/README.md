# Archived tasks (off-leaderboard, still runnable)

These v1 tasks are excluded from the v2 matrix and scoring: the runner and preflight glob
only the direct children of `tasks/`, so anything under `tasks/_archive/` is skipped. They
remain runnable ad-hoc (`bash run_one.sh <harness> _archive/<id> ...` won't resolve — copy
back to `tasks/` to run) and preserve v1 reproducibility (nothing deleted).

Selection: the 3 lowest-value floor tasks (fizzbuzz, email_extract, stack_debug — all 5/5,
non-discriminating) and 9 redundant near-duplicate cluster members from the boltons_/
littleutils_ real-repo clusters (all 5/5 in the v1 pi run; the discriminating members of
each cluster were kept). Retiring them brings the suite to the v2 target margins
(d1-2 = 20, d3 = 50) without dropping any capability the kept members still cover.
