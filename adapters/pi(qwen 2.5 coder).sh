#!/usr/bin/env bash
# Harness label: "pi(qwen 2.5 coder)"
# Identical behavior to the pi adapter — this is just a differently-named entry point so that
# a run of pi against the Qwen2.5-Coder-7B server profile is tagged "pi(qwen 2.5 coder)" in the
# harness column of out/results.csv (distinct from the Gemma "pi" run) while sharing the same
# results dataset. All logic lives in pi.sh; this delegates verbatim.
exec bash "$(dirname "$0")/pi.sh" "$@"
