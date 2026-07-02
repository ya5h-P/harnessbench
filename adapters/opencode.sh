#!/usr/bin/env bash
# opencode adapter. subcommands: invoke <workdir> <promptfile> <outdir> | metrics <workdir> <outdir>
# NOTE: launch the exe directly (NOT the PowerShell .ps1 wrapper, which hangs at init on Windows).
HB="$(cd "$(dirname "$0")/.." && pwd)"
OC="${OPENCODE_EXE:-/c/Users/User/AppData/Local/hermes/node/node_modules/opencode-ai/bin/opencode.exe}"
MODEL="${OPENCODE_MODEL:-llama.cpp/Qwen3.5-9B}"

cmd="$1"; workdir="$2"
if [ "$cmd" = "invoke" ]; then
  promptfile="$3"; outdir="$4"; prompt="$(cat "$promptfile")"
  ( cd "$workdir" && "$OC" run "$prompt" -m "$MODEL" ) > "$outdir/run.log" 2>&1
  exit $?
elif [ "$cmd" = "metrics" ]; then
  outdir="$3"
  "${HB_PYTHON:-python}" "$HB/adapters/parse_opencode.py" "$outdir/run.log" "$workdir"
fi
