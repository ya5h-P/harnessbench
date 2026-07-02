#!/usr/bin/env python3
"""Parse a pi `--mode json` JSONL run -> uniform metrics line.
usage: parse_pi.py <run.json>
prints: toolcalls=N turns=N out_tokens=N self_verify=0|1 tools=a,b,c
"""
import sys, json

EXEC = {"bash", "shell", "run", "exec", "python", "pytest", "test", "execute"}
WRITE = {"write", "edit", "create", "str_replace", "apply_patch", "patch", "multiedit"}

def main():
    path = sys.argv[1]
    turns = toolcalls = out_tokens = 0
    tools = []
    try:
        lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
    except Exception:
        print("toolcalls=0 turns=0 out_tokens=0 self_verify=0 tools=-"); return
    for ln in lines:
        ln = ln.strip()
        if not ln:
            continue
        try:
            o = json.loads(ln)
        except Exception:
            continue
        t = o.get("type")
        if t == "turn_start":
            turns += 1
        elif t == "tool_execution_start":
            nm = o.get("name") or o.get("toolName") or (o.get("toolCall") or {}).get("name")
            toolcalls += 1
            tools.append((nm or "?").lower())
        elif t == "message_end":
            m = o.get("message", {})
            if m.get("role") == "assistant":
                out_tokens += (m.get("usage") or {}).get("output", 0) or 0

    # self_verify: an exec-ish tool after the last write-ish tool
    last_write = max([i for i, t in enumerate(tools) if t in WRITE], default=-1)
    sv = 1 if any(t in EXEC for t in tools[last_write + 1:]) and last_write >= 0 else 0
    # also count "ran something at all" if no writes but executed (e.g., data tasks)
    if last_write < 0 and any(t in EXEC for t in tools):
        sv = 1
    print("toolcalls=%d turns=%d out_tokens=%d self_verify=%d tools=%s"
          % (toolcalls, turns, out_tokens, sv, ",".join(tools) if tools else "-"))

if __name__ == "__main__":
    main()
