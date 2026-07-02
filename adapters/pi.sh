#!/usr/bin/env bash
# pi adapter.  subcommands: invoke <workdir> <promptfile> <outdir> | metrics <workdir> <outdir>
HB="$(cd "$(dirname "$0")/.." && pwd)"
NODE="${PI_NODE:-/c/Users/User/AppData/Local/hermes/node/node.exe}"
CLI="${PI_CLI:-/c/Users/User/AppData/Local/hermes/node/node_modules/@earendil-works/pi-coding-agent/dist/cli.js}"

cmd="$1"; workdir="$2"
if [ "$cmd" = "invoke" ]; then
  promptfile="$3"; outdir="$4"; prompt="$(cat "$promptfile")"
  ( cd "$workdir" && "$NODE" "$CLI" -p --mode json "$prompt" ) > "$outdir/run.json" 2> "$outdir/run.err"
  exit $?
elif [ "$cmd" = "metrics" ]; then
  outdir="$3"
  "${HB_PYTHON:-python}" "$HB/adapters/parse_pi.py" "$outdir/run.json"
fi
