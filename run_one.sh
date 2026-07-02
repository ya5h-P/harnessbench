#!/usr/bin/env bash
# Run a single (harness, task, repeat, seed). Sets up isolated dirs, invokes the harness with a
# hard timeout, classifies the outcome, grades objectively, collects metrics, probes tok/s, and
# appends one row to out/results.csv.
#
# usage: run_one.sh <harness> <task_id> <repeat> <seed> [no_probe]
set -u
HB="$(cd "$(dirname "$0")" && pwd)"
PY="${HB_PYTHON:-python}"
harness="$1"; task="$2"; repeat="$3"; seed="$4"; noprobe="${5:-}"
taskdir="$HB/tasks/$task"
adapter="$HB/adapters/$harness.sh"
[ -f "$taskdir/task.json" ] || { echo "no such task: $task" >&2; exit 2; }
[ -f "$adapter" ] || { echo "no such harness adapter: $harness" >&2; exit 2; }

field(){ "$PY" -c "import json,sys;print(json.load(sys.stdin).get('$1',''))" < "$taskdir/task.json"; }
domain=$(field domain); difficulty=$(field difficulty); timeout_s=$(field timeout_s)
[ -z "$timeout_s" ] && timeout_s=480

rundir="$HB/runs/$harness/$task/rep$repeat"
rm -rf "$rundir"; mkdir -p "$rundir"
work="$rundir/work"; grade="$rundir/grade"; mkdir -p "$work" "$grade"

# 1. materialize agent-visible fixtures. Hidden grade files go to a throwaway temp dir here:
#    the real gradedir stays EMPTY while the agent runs (so it can't be read from ../grade) and
#    is regenerated deterministically from the same seed in step 3.
gtmp=$(mktemp -d)
"$PY" "$HB/engine/setup.py" "$taskdir" "$work" "$gtmp" "$seed" "" >/dev/null 2>&1
rm -rf "$gtmp"
cp "$taskdir/prompt.txt" "$rundir/prompt.txt"

# 2. invoke harness with hard timeout
# HB_TASKDIR points at grade.py/hidden/ref — only the mock dry-run adapter may see it; never
# leak it into a real harness's environment.
if [ "$harness" = "mock" ]; then export HB_TASKDIR="$taskdir"; else unset HB_TASKDIR; fi
start=$(date +%s)
timed_out=0; invoke_rc=0
if command -v timeout >/dev/null 2>&1; then
  timeout --kill-after=15 "${timeout_s}s" bash "$adapter" invoke "$work" "$rundir/prompt.txt" "$rundir"
  invoke_rc=$?
  [ "$invoke_rc" -eq 124 ] && timed_out=1
else
  bash "$adapter" invoke "$work" "$rundir/prompt.txt" "$rundir" &
  pid=$!; deadline=$(( $(date +%s) + timeout_s ))
  while kill -0 "$pid" 2>/dev/null; do
    [ "$(date +%s)" -ge "$deadline" ] && { kill -9 "$pid" 2>/dev/null; timed_out=1; break; }
    sleep 2
  done
  wait "$pid" 2>/dev/null; invoke_rc=$?
fi
end=$(date +%s); wall=$((end-start))

# 3. materialize hidden grade files (deferred from step 1; also defends against agent edits)
"$PY" "$HB/engine/setup.py" "$taskdir" "$grade.tmp" "$grade" "$seed" "" >/dev/null 2>&1 || true
rm -rf "$grade.tmp"

# 4. grade
gout=$("$PY" "$taskdir/grade.py" "$work" "$grade" 2>&1); grc=$?

# 5. classify outcome
logfile="$rundir/run.json"; [ -f "$logfile" ] || logfile="$rundir/run.log"
logsize=$(wc -c < "$logfile" 2>/dev/null || echo 0)
if [ "$grc" -eq 0 ]; then status=PASS; passed=1
else
  passed=0
  # CRASH is checked before REFUSED: a harness that dies before writing any log is a crash,
  # not a refusal (refusal = clean exit with an empty/near-empty log).
  if [ "$timed_out" -eq 1 ]; then status=TIMEOUT
  elif [ "$invoke_rc" -ne 0 ]; then status=CRASH
  elif [ "${logsize:-0}" -lt 5 ]; then status=REFUSED
  else status=WRONG; fi
fi

# 6. metrics
metrics=$(bash "$adapter" metrics "$work" "$rundir" 2>/dev/null)
get(){ echo "$metrics" | grep -oE "$1=[0-9]+" | head -1 | cut -d= -f2; }
toolcalls=$(get toolcalls); turns=$(get turns); out_tokens=$(get out_tokens); sv=$(get self_verify)
: "${toolcalls:=0}" "${turns:=0}" "${out_tokens:=0}" "${sv:=0}"

# 6b. integrity scan: flag any sign the agent reached for the task dir (grade.py/hidden/ref)
# or a grade dir. The gradedir is empty during the run, so this can't leak answers — but a
# harness that goes looking should be reviewed, not silently scored.
flags=""
if grep -qE "tasks[/\\\\]+$task[/\\\\]+(grade\.py|hidden|ref)" "$logfile" 2>/dev/null; then flags="taskdir-access"; fi
if grep -qE "(\.\.|rep$repeat)[/\\\\]+grade" "$logfile" 2>/dev/null; then flags="$flags gradedir-access"; fi
if [ -n "$flags" ]; then
  mkdir -p "$HB/out"
  [ -f "$HB/out/flags.csv" ] || echo "harness,task,repeat,flags" > "$HB/out/flags.csv"
  echo "$harness,$task,$repeat,$flags" >> "$HB/out/flags.csv"
  echo "  WARN: possible grader access:$flags (recorded in out/flags.csv)"
fi

# 7. tok/s probe (server now idle)
tokps=0
if [ "$noprobe" != "noprobe" ]; then
  pline=$(bash "$HB/probe_tokps.sh" "${harness}_${task}_r${repeat}" 2>/dev/null | tail -1)
  tokps=$(echo "$pline" | cut -d, -f3); : "${tokps:=0}"
fi

# 8. record
RES="$HB/out/results.csv"
mkdir -p "$HB/out"
[ -f "$RES" ] || echo "harness,task,domain,difficulty,repeat,seed,status,pass,wall_s,toolcalls,turns,out_tokens,self_verify,tokps" > "$RES"
echo "$harness,$task,$domain,$difficulty,$repeat,$seed,$status,$passed,$wall,$toolcalls,$turns,$out_tokens,$sv,$tokps" >> "$RES"
echo "[$harness/$task rep$repeat] $status pass=$passed wall=${wall}s tools=$toolcalls turns=$turns out_tok=$out_tokens sv=$sv tokps=$tokps"
echo "  grade: $gout" | head -1
