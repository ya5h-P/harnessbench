#!/usr/bin/env bash
# Discrimination guarantee: for every task, the hidden grader must FAIL the unsolved
# state and PASS the reference solution. Reseeded tasks must produce differing expected
# values across seeds. No harness/model is involved.
set -u
HB="$(cd "$(dirname "$0")/.." && pwd)"
PY="${HB_PYTHON:-python}"
TASKS_DIR="$HB/tasks"
TMP="$HB/.preflight"
rm -rf "$TMP"; mkdir -p "$TMP"
only="${1:-}"   # optional task-id filter

pass=0; fail=0; failed_ids=""
for taskdir in "$TASKS_DIR"/*/; do
  [ -f "$taskdir/task.json" ] || continue
  id=$(basename "$taskdir")
  [ -n "$only" ] && [ "$only" != "$id" ] && continue

  reseed=$("$PY" -c "import json,sys;print(1 if json.load(sys.stdin).get('reseed') else 0)" < "$taskdir/task.json" 2>/dev/null)

  # Rule 1 (v2): a task whose failures implicate no harness capability ("floor") must stay d1-2
  floorbad=$("$PY" -c "import json,sys;t=json.load(sys.stdin);print(1 if t.get('capability')=='floor' and t.get('difficulty',1)>=3 else 0)" < "$taskdir/task.json" 2>/dev/null)
  if [ "$floorbad" = "1" ]; then
    fail=$((fail+1)); failed_ids="$failed_ids $id"
    printf "  FAIL %-26s -> floor-capability-at-d>=3 (Rule 1: floor tasks are capped at d2)\n" "$id"
    continue
  fi

  # --- FAIL check (unsolved) ---
  wb="$TMP/$id/buggy/work"; gb="$TMP/$id/buggy/grade"; rm -rf "$TMP/$id"; mkdir -p "$wb" "$gb"
  variant_b=""; [ -d "$taskdir/buggy" ] && variant_b="buggy"
  "$PY" "$HB/engine/setup.py" "$taskdir" "$wb" "$gb" 1 "$variant_b" >/dev/null 2>&1
  out_b=$("$PY" "$taskdir/grade.py" "$wb" "$gb" 2>&1); rc_b=$?

  # --- PASS check (reference) ---
  wr="$TMP/$id/ref/work"; gr="$TMP/$id/ref/grade"; mkdir -p "$wr" "$gr"
  "$PY" "$HB/engine/setup.py" "$taskdir" "$wr" "$gr" 1 "ref" >/dev/null 2>&1
  # reference solver for tasks whose deliverable is a generated artifact (seed-dependent)
  if [ -f "$taskdir/ref/solve.py" ]; then ( cd "$wr" && "$PY" "$taskdir/ref/solve.py" "$wr" >/dev/null 2>&1 ); fi
  out_r=$("$PY" "$taskdir/grade.py" "$wr" "$gr" 2>&1); rc_r=$?

  ok=1; why=""
  if [ "$rc_b" -eq 0 ]; then ok=0; why="$why buggy-should-fail-but-passed"; fi
  if [ "$rc_r" -ne 0 ]; then ok=0; why="$why ref-should-pass-but-failed[$out_r]"; fi

  # --- reseed checks: different seeds must differ; the SAME seed must regenerate identical
  #     expected values (grading materializes the gradedir after the run from the run's seed) ---
  if [ "$reseed" = "1" ]; then
    e1="$TMP/$id/s1g"; e2="$TMP/$id/s2g"; e3="$TMP/$id/s3g"
    mkdir -p "$TMP/$id/s1w" "$e1" "$TMP/$id/s2w" "$e2" "$TMP/$id/s3w" "$e3"
    "$PY" "$HB/engine/setup.py" "$taskdir" "$TMP/$id/s1w" "$e1" 101 "" >/dev/null 2>&1
    "$PY" "$HB/engine/setup.py" "$taskdir" "$TMP/$id/s2w" "$e2" 202 "" >/dev/null 2>&1
    "$PY" "$HB/engine/setup.py" "$taskdir" "$TMP/$id/s3w" "$e3" 101 "" >/dev/null 2>&1
    h1=$(cat "$e1"/* 2>/dev/null | "$PY" -c "import sys,hashlib;print(hashlib.md5(sys.stdin.buffer.read()).hexdigest())")
    h2=$(cat "$e2"/* 2>/dev/null | "$PY" -c "import sys,hashlib;print(hashlib.md5(sys.stdin.buffer.read()).hexdigest())")
    h3=$(cat "$e3"/* 2>/dev/null | "$PY" -c "import sys,hashlib;print(hashlib.md5(sys.stdin.buffer.read()).hexdigest())")
    [ "$h1" = "$h2" ] && { ok=0; why="$why reseed-did-not-change-expected"; }
    [ "$h1" != "$h3" ] && { ok=0; why="$why same-seed-not-deterministic"; }
  fi

  if [ "$ok" -eq 1 ]; then
    pass=$((pass+1)); printf "  OK   %-26s (buggy rc=%s, ref rc=%s)\n" "$id" "$rc_b" "$rc_r"
  else
    fail=$((fail+1)); failed_ids="$failed_ids $id"; printf "  FAIL %-26s ->%s\n" "$id" "$why"
  fi
done
echo "-----------------------------------------"
echo "preflight: $pass ok, $fail failing.${failed_ids:+ FAILED:$failed_ids}"
[ "$fail" -eq 0 ]
