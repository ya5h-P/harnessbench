#!/usr/bin/env bash
# hermes adapter. subcommands: invoke <workdir> <promptfile> <outdir> | metrics <workdir> <outdir>
HB="$(cd "$(dirname "$0")/.." && pwd)"
HERMES="${HERMES_EXE:-/c/Users/User/AppData/Local/hermes/hermes-agent/venv/Scripts/hermes.exe}"

cmd="$1"; workdir="$2"
if [ "$cmd" = "invoke" ]; then
  promptfile="$3"; outdir="$4"; prompt="$(cat "$promptfile")"
  ( cd "$workdir" && "$HERMES" -z "$prompt" --yolo --cli ) > "$outdir/run.log" 2>&1
  exit $?
elif [ "$cmd" = "metrics" ]; then
  outdir="$3"
  "${HB_PYTHON:-python}" "$HB/adapters/parse_hermes.py" "$workdir" "$outdir/run.log"
fi
