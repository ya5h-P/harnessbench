"""Delta of llama.cpp /metrics counters between two snapshots.

Usage: metrics_delta.py before.prom after.prom
Prints: prompt_tokens gen_tokens prompt_seconds gen_seconds gen_tokps
All zeros if either snapshot is missing/empty (caller falls back to the probe).
"""
import re
import sys


def parse(path):
    vals = {}
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            for line in f:
                m = re.match(r"llamacpp:([A-Za-z_]+)\s+([0-9.eE+-]+)\s*$", line.strip())
                if m:
                    vals[m.group(1)] = float(m.group(2))
    except OSError:
        pass
    return vals


a, b = parse(sys.argv[1]), parse(sys.argv[2])


def delta(key):
    if key not in a or key not in b:
        return 0.0
    return max(0.0, b[key] - a[key])


pt = delta("prompt_tokens_total")
gt = delta("tokens_predicted_total")
ps = delta("prompt_seconds_total")
gs = delta("tokens_predicted_seconds_total")
tokps = gt / gs if gs > 0 else 0.0
print("%d %d %.2f %.2f %.2f" % (pt, gt, ps, gs, tokps))
