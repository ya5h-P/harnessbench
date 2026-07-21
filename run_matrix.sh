#!/usr/bin/env bash
# Orchestrate the full benchmark matrix. Sequential (single-concurrency endpoint), resumable
# (out/results.csv is the checkpoint), randomized order, with one discarded warmup per harness.
#
# usage: run_matrix.sh [--harness pi,opencode,hermes] [--tasks all|id,id] [--repeats N]
#                      [--seed-base S] [--no-warmup] [--no-probe] [--reset]
set -u
HB="$(cd "$(dirname "$0")" && pwd)"
PY="${HB_PYTHON:-python}"

HARNESSES="pi,opencode,hermes"; TASKS="all"; REPEATS=5; SEEDBASE=1000; WARMUP=1; PROBE=""; RESET=0
while [ $# -gt 0 ]; do
  case "$1" in
    --harness) HARNESSES="$2"; shift 2;;
    --tasks) TASKS="$2"; shift 2;;
    --repeats) REPEATS="$2"; shift 2;;
    --seed-base) SEEDBASE="$2"; shift 2;;
    --no-warmup) WARMUP=0; shift;;
    --no-probe) PROBE="noprobe"; shift;;
    --reset) RESET=1; shift;;
    *) echo "unknown arg $1"; exit 2;;
  esac
done

# --reset: wipe the checkpoint (results.csv) and the per-run outputs the matrix appends to, then
# EXIT. It never launches a run, so it can't assume a harness/task/repeat set you didn't ask for —
# re-run without --reset to actually start the matrix. Analysis artifacts (scores.json,
# LEADERBOARD.md, *.log, plots) are left alone. Destructive and irreversible, so it requires an
# explicit typed confirmation.
if [ "$RESET" -eq 1 ]; then
  echo "RESET will permanently delete the benchmark checkpoint and per-run outputs:"
  echo "  $HB/out/results.csv"
  echo "  $HB/out/server_usage.csv"
  echo "  $HB/out/flags.csv"
  echo "  $HB/runs/   (all per-run working dirs, logs, and grades)"
  echo "It will NOT touch scores.json, LEADERBOARD.md, *.log, or the plots."
  echo
  # Read the confirmation from the controlling terminal. FIRST drain any pending type-ahead: a
  # newline left in the input buffer (e.g. from the Enter that launched this command, or a paste)
  # would otherwise be read *as* the answer, which is what made an earlier run "abort" before
  # anything was typed. Then re-ask on a fumbled entry rather than aborting on the first slip; only
  # the exact word "yes" proceeds, and an empty line (or Ctrl-D) cancels.
  while IFS= read -r -t 0.1 _ </dev/tty 2>/dev/null; do :; done   # flush buffered input
  confirm=""
  while :; do
    printf 'This cannot be undone. Type "yes" to confirm (or Enter to cancel): '
    IFS= read -r confirm </dev/tty || { echo; confirm=""; }
    confirm=$(printf '%s' "$confirm" | tr -d '[:space:]' | tr '[:upper:]' '[:lower:]')
    [ "$confirm" = "yes" ] && break
    if [ -z "$confirm" ]; then echo "reset aborted (no changes made)."; exit 0; fi
    echo "  got '$confirm' — type exactly 'yes', or press Enter to cancel."
  done
  rm -f "$HB/out/results.csv" "$HB/out/server_usage.csv" "$HB/out/flags.csv"
  # runs/ can hold a working dir a lingering harness process (node/opencode/hermes) still has open,
  # which rm reports as "Device or resource busy". Capture that instead of falsely claiming success.
  rm_err=$(rm -rf "$HB/runs" 2>&1)
  if [ -n "$rm_err" ] || [ -d "$HB/runs" ]; then
    echo "reset INCOMPLETE: some paths could not be removed (a lingering harness process is"
    echo "probably still holding a working dir open):"
    [ -n "$rm_err" ] && echo "$rm_err" | sed 's/^/  /'
    echo "Kill any stray harness processes, e.g.:  taskkill //F //IM node.exe //IM opencode.exe"
    echo "then run './run_matrix.sh --reset' again."
    exit 1
  fi
  echo "reset complete. Re-run without --reset to start the matrix."
  exit 0
fi

# task list
if [ "$TASKS" = "all" ]; then
  mapfile -t TASK_IDS < <(for d in "$HB"/tasks/*/; do [ -f "$d/task.json" ] && basename "$d"; done | sort)
else
  IFS=',' read -ra TASK_IDS <<< "$TASKS"
fi
IFS=',' read -ra HLIST <<< "$HARNESSES"

RES="$HB/out/results.csv"
# match exact field positions (harness,task,domain,difficulty,repeat,seed,...) — a greedy .*
# here could false-match repeat/seed against later numeric columns and silently skip a run
done_key(){ grep -q "^$1,$2,[^,]*,[^,]*,$3,$4," "$RES" 2>/dev/null; }

echo "HarnessBench matrix: harnesses=[$HARNESSES] tasks=${#TASK_IDS[@]} repeats=$REPEATS"
[ -f "$RES" ] && echo "resuming; $(($(wc -l < "$RES")-1)) rows already present"

# build the run list (harness,task,repeat,seed)
RUNLIST=()
for h in "${HLIST[@]}"; do
  for t in "${TASK_IDS[@]}"; do
    for ((r=1; r<=REPEATS; r++)); do
      RUNLIST+=("$h|$t|$r|$((SEEDBASE + r))")
    done
  done
done

# deterministic-ish shuffle (interleave to spread thermal drift) without Math.random:
# sort by a hash of the line so order is stable but mixed across harness/task.
mapfile -t RUNLIST < <(for x in "${RUNLIST[@]}"; do
  hsh=$(echo "$x" | "$PY" -c "import sys,hashlib;print(hashlib.md5(sys.stdin.read().encode()).hexdigest())")
  echo "$hsh $x"
done | sort | cut -d' ' -f2-)

# warmup (discarded) per harness
if [ "$WARMUP" -eq 1 ]; then
  for h in "${HLIST[@]}"; do
    echo "== warmup $h (discarded) =="
    bash "$HB/run_one.sh" "$h" greet_format 0 1 noprobe >/dev/null 2>&1 || true
    rm -rf "$HB/runs/$h/greet_format/rep0"
  done
fi

i=0; n=${#RUNLIST[@]}
for entry in "${RUNLIST[@]}"; do
  IFS='|' read -r h t r s <<< "$entry"
  i=$((i+1))
  if done_key "$h" "$t" "$r" "$s"; then
    echo "[$i/$n] skip (done) $h/$t rep$r"; continue
  fi
  echo "[$i/$n] $h/$t rep$r seed$s"
  bash "$HB/run_one.sh" "$h" "$t" "$r" "$s" "$PROBE"
done

echo "matrix complete. score with:  python score.py"
