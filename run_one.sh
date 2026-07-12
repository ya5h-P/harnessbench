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
# snapshot llama.cpp /metrics counters so token counts + tok/s come from the harness's actual
# requests (server must run with --metrics; empty snapshots fall back to the probe below)
MURL="${HB_METRICS_URL:-http://localhost:8000/metrics}"
curl -s -m 3 "$MURL" 2>/dev/null | grep '^llamacpp:' > "$rundir/m0.prom" || true
# baseline generated-token counter for the runaway watchdog. The server is single-slot and runs
# are sequential, so (current - gen0) is THIS task's generated tokens across all its turns. If it
# blows past the runaway cap the harness is killed mid-flight and the run is classified RUNAWAY.
gen0=$(awk '/^llamacpp:tokens_predicted_total/{print int($2)}' "$rundir/m0.prom"); : "${gen0:=0}"
# /metrics' tokens_predicted_total only updates once a request completes, so a single pathological
# completion (a repetition loop generating tens of thousands of tokens in one turn) is invisible to
# the gen0/gcur delta below until it's already over — confirmed live via llama-server's own
# print_timing console log showing n_decoded climbing past 30k while /metrics stayed flat. /slots
# (enabled: endpoint_slots=true) exposes each in-flight request's live decode count instead, so it's
# checked first; the cumulative /metrics delta stays as a second check (catches many-small-turns-
# add-up-to-a-runaway, which a single request's n_decoded can't see) and as a fallback for servers
# without --slots.
SURL="${HB_SLOTS_URL:-${MURL%/metrics}/slots}"
RUNAWAY_TOKENS="${HB_RUNAWAY_TOKENS:-8000}"
start=$(date +%s)
timed_out=0; invoke_rc=0; runaway=0

# kill an MSYS background process AND its Windows child tree (the harness exe: node/hermes)
kill_tree(){
  local p="$1" wp
  wp=$(cat "/proc/$p/winpid" 2>/dev/null)
  [ -n "$wp" ] && taskkill //F //T //PID "$wp" >/dev/null 2>&1
  kill -9 "$p" 2>/dev/null
}

# single watchdog enforcing BOTH the wall-clock timeout and the token runaway cap
bash "$adapter" invoke "$work" "$rundir/prompt.txt" "$rundir" &
pid=$!; deadline=$(( start + timeout_s ))
while kill -0 "$pid" 2>/dev/null; do
  now=$(date +%s)
  if [ "$now" -ge "$deadline" ]; then kill_tree "$pid"; timed_out=1; break; fi
  # live check: in-flight request's own decode count (catches a single runaway completion
  # immediately, without waiting for the request to finish). /slots keeps the LAST completed
  # request's n_decoded even when idle, so this must gate on is_processing=true — otherwise a
  # fresh task reads the previous task's stale count and kills itself instantly.
  ndec=$(curl -s -m 3 "$SURL" 2>/dev/null | "$PY" -c '
import json,sys
try:
    slots = json.load(sys.stdin)
    vals = []
    for s in slots:
        if not s.get("is_processing"):
            continue
        nt = s.get("next_token") or {}
        if isinstance(nt, list):
            nt = nt[0] if nt else {}
        vals.append(nt.get("n_decoded", 0))
    print(max(vals) if vals else "")
except Exception:
    print("")
' 2>/dev/null)
  if [ -n "$ndec" ] && [ "$ndec" -gt "$RUNAWAY_TOKENS" ]; then
    kill_tree "$pid"; runaway=1; break
  fi
  # cumulative check: total tokens generated so far this task across all turns (fallback source
  # if /slots is unavailable)
  gcur=$(curl -s -m 3 "$MURL" 2>/dev/null | awk '/^llamacpp:tokens_predicted_total/{print int($2)}')
  if [ -n "$gcur" ] && [ "$((gcur - gen0))" -gt "$RUNAWAY_TOKENS" ]; then
    kill_tree "$pid"; runaway=1; break
  fi
  sleep 3
done
wait "$pid" 2>/dev/null; invoke_rc=$?
end=$(date +%s); wall=$((end-start))
curl -s -m 3 "$MURL" 2>/dev/null | grep '^llamacpp:' > "$rundir/m1.prom" || true

# 3. materialize hidden grade files (deferred from step 1; also defends against agent edits)
"$PY" "$HB/engine/setup.py" "$taskdir" "$grade.tmp" "$grade" "$seed" "" >/dev/null 2>&1 || true
rm -rf "$grade.tmp"

# 4. grade
gout=$("$PY" "$taskdir/grade.py" "$work" "$grade" 2>&1); grc=$?

# 5. classify outcome
logfile="$rundir/run.json"; [ -f "$logfile" ] || logfile="$rundir/run.log"
logsize=$(wc -c < "$logfile" 2>/dev/null || echo 0)
# RUNAWAY takes precedence: if we had to kill the harness for exceeding the token cap, the run is
# a runaway regardless of what partial output happened to grade as.
if [ "$runaway" -eq 1 ]; then status=RUNAWAY; passed=0
elif [ "$grc" -eq 0 ]; then status=PASS; passed=1
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

# 7. tok/s + token counts, measured from the run's own requests via /metrics deltas.
# When the server exposes metrics, out_tokens and tokps are server-side truth (includes every
# request the harness made, at real context depth); the synthetic probe is only a fallback.
tokps=0; tok_src=probe
read -r srv_prompt srv_gen srv_prompt_s srv_gen_s srv_tokps < <("$PY" "$HB/engine/metrics_delta.py" "$rundir/m0.prom" "$rundir/m1.prom" 2>/dev/null)
: "${srv_prompt:=0}" "${srv_gen:=0}" "${srv_prompt_s:=0}" "${srv_gen_s:=0}" "${srv_tokps:=0}"
if awk "BEGIN{exit !($srv_tokps > 0)}"; then
  tokps=$srv_tokps; out_tokens=$srv_gen; tok_src=server
  USAGE="$HB/out/server_usage.csv"
  [ -f "$USAGE" ] || echo "harness,task,repeat,prompt_tokens,gen_tokens,prompt_s,gen_s,gen_tokps" > "$USAGE"
  echo "$harness,$task,$repeat,$srv_prompt,$srv_gen,$srv_prompt_s,$srv_gen_s,$srv_tokps" >> "$USAGE"
elif [ "$noprobe" != "noprobe" ]; then
  pline=$(bash "$HB/probe_tokps.sh" "${harness}_${task}_r${repeat}" 2>/dev/null | tail -1)
  tokps=$(echo "$pline" | cut -d, -f3); : "${tokps:=0}"
fi

# 8. record
RES="$HB/out/results.csv"
mkdir -p "$HB/out"
[ -f "$RES" ] || echo "harness,task,domain,difficulty,repeat,seed,status,pass,wall_s,toolcalls,turns,out_tokens,self_verify,tokps" > "$RES"
echo "$harness,$task,$domain,$difficulty,$repeat,$seed,$status,$passed,$wall,$toolcalls,$turns,$out_tokens,$sv,$tokps" >> "$RES"
echo "[$harness/$task rep$repeat] $status pass=$passed wall=${wall}s tools=$toolcalls turns=$turns out_tok=$out_tokens sv=$sv tokps=$tokps (src=$tok_src)"
echo "  grade: $gout" | head -1
