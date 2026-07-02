#!/usr/bin/env bash
# MOCK harness for self-testing the pipeline WITHOUT a model. On invoke it plays a perfect agent:
# it overlays the task's ref/ solution into the workdir and runs ref/solve.py if present.
# metrics returns plausible fixed values. Use: run_one.sh mock <task> ...
cmd="$1"; workdir="$2"
if [ "$cmd" = "invoke" ]; then
  outdir="$4"
  if [ -n "${HB_TASKDIR:-}" ] && [ -d "$HB_TASKDIR/ref" ]; then
    cp -rf "$HB_TASKDIR/ref/." "$workdir/" 2>/dev/null
    [ -f "$workdir/solve.py" ] && [ ! -f "$HB_TASKDIR/fixtures/solve.py" ] && {
      ( cd "$workdir" && "${HB_PYTHON:-python}" solve.py "$workdir" >/dev/null 2>&1 ); rm -f "$workdir/solve.py"; }
  fi
  echo "mock: wrote reference solution and verified" > "$outdir/run.log"
  exit 0
elif [ "$cmd" = "metrics" ]; then
  echo "toolcalls=4 turns=4 out_tokens=300 self_verify=1 tools=read,write,bash,bash"
fi
