#!/usr/bin/env bash
# Orchestrate the full benchmark matrix. Sequential (single-concurrency endpoint), resumable
# (out/results.csv is the checkpoint), randomized order, with one discarded warmup per harness.
#
# usage: run_matrix.sh [--harness pi,opencode,hermes] [--tasks all|id,id] [--repeats N]
#                      [--seed-base S] [--no-warmup] [--no-probe]
set -u
HB="$(cd "$(dirname "$0")" && pwd)"
PY="${HB_PYTHON:-python}"

HARNESSES="pi,opencode,hermes"; TASKS="all"; REPEATS=5; SEEDBASE=1000; WARMUP=1; PROBE=""
while [ $# -gt 0 ]; do
  case "$1" in
    --harness) HARNESSES="$2"; shift 2;;
    --tasks) TASKS="$2"; shift 2;;
    --repeats) REPEATS="$2"; shift 2;;
    --seed-base) SEEDBASE="$2"; shift 2;;
    --no-warmup) WARMUP=0; shift;;
    --no-probe) PROBE="noprobe"; shift;;
    *) echo "unknown arg $1"; exit 2;;
  esac
done

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
