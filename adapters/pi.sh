#!/usr/bin/env bash
# pi adapter.  subcommands: invoke <workdir> <promptfile> <outdir> | metrics <workdir> <outdir>
HB="$(cd "$(dirname "$0")/.." && pwd)"
NODE="${PI_NODE:-/c/Users/User/AppData/Local/hermes/node/node.exe}"
CLI="${PI_CLI:-/c/Users/User/AppData/Local/hermes/node/node_modules/@earendil-works/pi-coding-agent/dist/cli.js}"

cmd="$1"; workdir="$2"
if [ "$cmd" = "invoke" ]; then
  promptfile="$3"; outdir="$4"; prompt="$(cat "$promptfile")"
  # Stream pi's JSONL through compact_pi.py so run.json keeps every message and
  # tool call but drops the O(N^2) `message_update` redundancy.  PIPESTATUS[0]
  # preserves pi's own exit code (not the filter's).
  ( cd "$workdir" && "$NODE" "$CLI" -p --mode json "$prompt" ) 2> "$outdir/run.err" \
    | "${HB_PYTHON:-python}" "$HB/adapters/compact_pi.py" > "$outdir/run.json"
  exit "${PIPESTATUS[0]}"
elif [ "$cmd" = "metrics" ]; then
  outdir="$3"
  "${HB_PYTHON:-python}" "$HB/adapters/parse_pi.py" "$outdir/run.json"
fi
