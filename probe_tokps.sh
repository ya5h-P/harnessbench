#!/usr/bin/env bash
# Fixed-workload tok/s probe against the (idle) local model server. Records throughput so the
# Efficiency score normalizes out model/server speed. Arg1: label. Env: HB_ENDPOINT, HB_MODEL.
label="${1:-probe}"
HB="$(cd "$(dirname "$0")" && pwd)"
CSV="$HB/out/tokps.csv"
ENDPOINT="${HB_ENDPOINT:-http://localhost:8000/v1/chat/completions}"
MODEL="${HB_MODEL:-Qwen3.5-9B}"
ts=$(date +%H:%M:%S)
body='{"model":"'"$MODEL"'","messages":[{"role":"user","content":"Write a short paragraph about the number seven and its history."}],"max_tokens":256,"temperature":0.6,"stream":false}'
resp=$(curl -s "$ENDPOINT" -H "Content-Type: application/json" -d "$body" 2>/dev/null)
line=$(echo "$resp" | "${HB_PYTHON:-python}" -c "
import json,sys
try: d=json.load(sys.stdin)
except Exception: print('$label,$ts,0,0,0,0'); sys.exit()
t=d.get('timings',{}) or {}
pps=t.get('predicted_per_second',0) or 0; pn=t.get('predicted_n',0) or 0
prs=t.get('prompt_per_second',0) or 0
dn=t.get('draft_n',0) or 0; da=t.get('draft_n_accepted',0) or 0
acc=(da/dn) if dn else 0
# fall back to usage if timings absent (non-llama.cpp servers)
if not pps:
    u=d.get('usage',{}) or {}; pn=u.get('completion_tokens',0) or 0
print('%s,%s,%.2f,%d,%.2f,%.3f' % ('$label','$ts',pps,pn,prs,acc))
")
mkdir -p "$HB/out"
[ -f "$CSV" ] || echo "label,time,gen_tokps,gen_tokens,prompt_tokps,draft_accept" > "$CSV"
echo "$line" | tee -a "$CSV"
