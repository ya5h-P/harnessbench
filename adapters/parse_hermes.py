#!/usr/bin/env python3
"""Best-effort parse of hermes state.db -> uniform metrics line.
usage: parse_hermes.py <workdir> [run.log]
prints: toolcalls=N turns=N out_tokens=N self_verify=0|1 tools=a,b,c
hermes strips tool calls from -z/--cli stdout, so metrics come from state.db when available.
"""
import sys, os, sqlite3, json, re

EXEC = {"bash", "shell", "terminal", "run", "exec", "python", "code_execution", "execute"}
WRITE = {"write", "edit", "create", "str_replace", "apply_patch", "file", "write_file", "edit_file"}

def db_path():
    for p in [os.path.join(os.environ.get("LOCALAPPDATA", ""), "hermes", "state.db"),
              os.path.expanduser("~/.hermes/state.db")]:
        if os.path.exists(p):
            return p
    return None

def extract_tools(data):
    """Pull tool names (in order) from a hermes message JSON blob."""
    names = []
    try:
        obj = json.loads(data) if isinstance(data, str) else data
    except Exception:
        return names
    def walk(x):
        if isinstance(x, dict):
            if x.get("type") in ("tool_use", "tool_call", "function_call") or "tool_name" in x:
                nm = x.get("name") or x.get("tool_name") or (x.get("function") or {}).get("name")
                if nm:
                    names.append(str(nm).lower())
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(obj)
    return names

def main():
    workdir = sys.argv[1]
    tools = []
    turns = out_tokens = 0
    dbp = db_path()
    if dbp:
        try:
            con = sqlite3.connect(dbp); con.row_factory = sqlite3.Row; cur = con.cursor()
            cur.execute("PRAGMA table_info(sessions)")
            scols = [r[1] for r in cur.fetchall()]
            # newest session (optionally matching workdir if a path column exists)
            order = "rowid"
            for c in ("updated_at", "created_at", "time_updated", "id"):
                if c in scols:
                    order = c; break
            sid = None
            cur.execute("SELECT * FROM sessions ORDER BY %s DESC LIMIT 50" % order)
            rows = cur.fetchall()
            wdbase = os.path.basename(os.path.abspath(workdir)).lower()
            for r in rows:
                vals = " ".join(str(r[c]).lower() for c in scols if r[c] is not None)
                if wdbase in vals or os.path.abspath(workdir).replace("\\", "/").lower() in vals:
                    sid = r["id"] if "id" in scols else r[0]; break
            if sid is None and rows:
                sid = rows[0]["id"] if "id" in scols else rows[0][0]

            cur.execute("PRAGMA table_info(messages)")
            mcols = [r[1] for r in cur.fetchall()]
            datacol = next((c for c in ("data", "content", "message", "body", "json") if c in mcols), None)
            sidcol = next((c for c in ("session_id", "sessionId", "session") if c in mcols), None)
            if datacol and sidcol and sid is not None:
                cur.execute("SELECT %s AS d FROM messages WHERE %s=? ORDER BY rowid" % (datacol, sidcol), (sid,))
                for m in cur.fetchall():
                    nm = extract_tools(m["d"])
                    if nm:
                        tools.extend(nm); turns += 1
                    # rough token estimate from text length if usage absent
        except Exception:
            pass

    toolcalls = len(tools)
    last_write = max([i for i, t in enumerate(tools) if t in WRITE], default=-1)
    sv = 1 if (last_write >= 0 and any(t in EXEC for t in tools[last_write + 1:])) else (
        1 if (last_write < 0 and any(t in EXEC for t in tools)) else 0)
    print("toolcalls=%d turns=%d out_tokens=%d self_verify=%d tools=%s"
          % (toolcalls, turns, out_tokens, sv, ",".join(tools) if tools else "-"))

if __name__ == "__main__":
    main()
