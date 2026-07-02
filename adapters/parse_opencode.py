#!/usr/bin/env python3
"""Parse an opencode `run` log + its SQLite session DB -> uniform metrics line.
usage: parse_opencode.py <run.log> <workdir>
prints: toolcalls=N turns=N out_tokens=N self_verify=0|1 tools=a,b,c
"""
import sys, os, re, sqlite3, glob

def db_path():
    for p in [os.path.expanduser("~/.local/share/opencode/opencode.db"),
              os.path.join(os.environ.get("LOCALAPPDATA", ""), "opencode", "opencode.db")]:
        if os.path.exists(p):
            return p
    return None

def main():
    runlog, workdir = sys.argv[1], sys.argv[2]
    tools = []
    try:
        raw = open(runlog, encoding="utf-8", errors="replace").read()
    except Exception:
        raw = ""
    raw = re.sub(r"\x1b\[[0-9;]*m", "", raw)
    for line in raw.splitlines():
        s = line.strip()
        if s.startswith("→"):       # -> Read
            tools.append("read")
        elif s.startswith("←"):     # <- Write/Edit
            tools.append("write")
        elif s.startswith("$"):          # $ shell command
            tools.append("bash")
    toolcalls = len(tools)
    last_write = max([i for i, t in enumerate(tools) if t == "write"], default=-1)
    sv = 1 if (last_write >= 0 and "bash" in tools[last_write + 1:]) else (1 if last_write < 0 and "bash" in tools else 0)

    turns = out_tokens = 0
    dbp = db_path()
    if dbp:
        try:
            con = sqlite3.connect(dbp); con.row_factory = sqlite3.Row; cur = con.cursor()
            wd = os.path.abspath(workdir).replace("\\", "/").lower()
            cur.execute("SELECT id, tokens_output, directory, time_created FROM session ORDER BY time_created DESC LIMIT 200")
            for r in cur.fetchall():
                d = (r["directory"] or "").replace("\\", "/").lower()
                if d.endswith(wd) or wd.endswith(d.split("/")[-1]) and os.path.basename(wd) in d:
                    out_tokens = r["tokens_output"] or 0
                    cur.execute("SELECT COUNT(*) c FROM message WHERE session_id=?", (r["id"],))
                    turns = cur.fetchone()["c"] or 0
                    break
        except Exception:
            pass
    print("toolcalls=%d turns=%d out_tokens=%d self_verify=%d tools=%s"
          % (toolcalls, turns, out_tokens, sv, ",".join(tools) if tools else "-"))

if __name__ == "__main__":
    main()
