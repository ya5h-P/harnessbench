#!/usr/bin/env python3
"""Score HarnessBench results with fixed, absolute-anchor rubrics (a new harness never changes
existing harnesses' scores). Emits out/scores.json and out/LEADERBOARD.md.

Categories (0-100): Correctness, Reliability, Efficiency, Capability.
Composite (default weights): 0.35 Correctness + 0.25 Reliability + 0.20 Efficiency + 0.20 Capability.

Near-duplicate tasks are grouped into clusters (see CLUSTER_PREFIXES): every mean is
cluster-weighted, the CI is a cluster bootstrap, and harness pairs get a paired sign-flip
permutation test on per-cluster pass rates.
"""
import sys, os, csv, json, statistics, random
from collections import Counter

HB = os.path.dirname(os.path.abspath(__file__))
WEIGHTS = {"correctness": 0.35, "reliability": 0.25, "efficiency": 0.20, "capability": 0.20}
ADHERENCE_DOMAINS = {"instruction-format-adherence", "spec-to-cli", "serialization-roundtrip"}

# Task clusters: tasks sharing a prefix are one parameterized family (the same skill at scaling
# load) — statistically one skill, not N independent tasks. Each cluster gets total weight 1
# (split among its members), and the bootstrap resamples clusters, because tasks within a
# cluster are correlated and treating them as independent would understate the CI and
# overweight the skill.
CLUSTER_PREFIXES = ("littleutils_", "boltons_",
                    "needle_", "bigfile_", "multiedit_", "exactout_", "chain_", "weirdfs_",
                    "manyfix_", "readdocs_", "logdig_", "testfix_", "editfid_")

def cluster_of(task_id):
    for p in CLUSTER_PREFIXES:
        if task_id.startswith(p):
            return p.rstrip("_")
    return task_id

def weights_for(ids):
    """Per-task weight 1/|cluster| so every cluster contributes equally. Bootstrap keys are
    'task#draw'; the draw tag keeps two draws of the same cluster as separate clusters."""
    ckey = {}
    for t in ids:
        base, _, tag = t.partition("#")
        ckey[t] = cluster_of(base) + ("#" + tag if tag else "")
    sizes = Counter(ckey.values())
    return {t: 1.0 / sizes[ckey[t]] for t in ids}

def interp(x, anchors):
    """Piecewise-linear map from x to score using sorted (x,score) anchors (absolute)."""
    anchors = sorted(anchors)
    if x <= anchors[0][0]:
        return anchors[0][1]
    if x >= anchors[-1][0]:
        return anchors[-1][1]
    for (x0, y0), (x1, y1) in zip(anchors, anchors[1:]):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return anchors[-1][1]

# absolute anchors
EFF_ANCHORS = [(1.0, 100), (1.5, 92), (2.0, 84), (3.0, 68), (5.0, 45), (8.0, 22), (12.0, 8), (20.0, 3)]
EFF_FALLBACK = [(20, 100), (45, 85), (80, 68), (140, 45), (240, 22), (400, 8)]   # wall_s / difficulty

def load(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            for k in ("difficulty", "repeat", "pass", "wall_s", "toolcalls", "turns",
                      "out_tokens", "self_verify"):
                r[k] = float(r[k]) if r.get(k) not in (None, "") else 0.0
            r["tokps"] = float(r["tokps"]) if r.get("tokps") not in (None, "") else 0.0
            if r["repeat"] == 0:
                continue   # repeat 0 = discarded warmup run; never scored
            rows.append(r)
    return rows

def task_aggregate(reps):
    """Aggregate repeats of one (harness,task) -> dict of stats."""
    passes = [r["pass"] for r in reps]
    clean = [0.0 if r["status"] in ("CRASH", "TIMEOUT", "REFUSED") else 1.0 for r in reps]
    sv = [r["self_verify"] for r in reps]
    has_tools = any(r["toolcalls"] > 0 for r in reps)
    walls = [r["wall_s"] for r in reps]
    outs = [r["out_tokens"] for r in reps]
    tps = [r["tokps"] for r in reps if r["tokps"] > 0]
    med_wall = statistics.median(walls) if walls else 0
    med_out = statistics.median(outs) if outs else 0
    med_tps = statistics.median(tps) if tps else 0
    # overhead ratio R (per task) for efficiency
    if med_out > 0 and med_tps > 0:
        R = med_wall / (med_out / med_tps)
        eff = interp(R, EFF_ANCHORS)
        eff_mode = "overhead"
    else:
        diff = reps[0]["difficulty"] or 1
        eff = interp(med_wall / diff, EFF_FALLBACK)
        eff_mode = "wallclock"
    return {
        "difficulty": reps[0]["difficulty"], "domain": reps[0]["domain"],
        "pass_rate": sum(passes) / len(passes),
        "pass_all": 1.0 if all(p >= 1 for p in passes) else 0.0,
        "pass_any": 1.0 if any(p >= 1 for p in passes) else 0.0,
        "clean_rate": sum(clean) / len(clean),
        "self_verify_rate": sum(sv) / len(sv),
        "has_tools": has_tools,
        "med_wall": med_wall, "eff": eff, "eff_mode": eff_mode, "n": len(reps),
    }

def categories(tasks):
    """tasks: dict task_id -> aggregate. Returns the four category scores 0-100.
    All means/weights are cluster-weighted (see weights_for)."""
    ids = list(tasks)
    w = weights_for(ids)

    def wmean(sub_ids, key):
        tw = sum(w[t] for t in sub_ids) or 1
        return sum(w[t] * tasks[t][key] for t in sub_ids) / tw

    dw = {t: tasks[t]["difficulty"] * w[t] for t in ids}
    wsum = sum(dw.values()) or 1
    correctness = 100 * sum(dw[t] * tasks[t]["pass_rate"] for t in ids) / wsum
    hard = [t for t in ids if tasks[t]["difficulty"] >= 4]
    if hard:
        hw = sum(dw[t] for t in hard) or 1
        capability = 100 * sum(dw[t] * tasks[t]["pass_rate"] for t in hard) / hw
    else:
        capability = correctness
    consistency = wmean(ids, "pass_all")
    clean = wmean(ids, "clean_rate")
    adh_ids = [t for t in ids if tasks[t]["domain"] in ADHERENCE_DOMAINS]
    adherence = wmean(adh_ids, "pass_rate") if adh_ids else consistency
    # self-verify only counts when the harness exposes tool instrumentation; otherwise drop the
    # term and renormalize the remaining weights so a partially-instrumented harness isn't penalized.
    comps = [(0.40, consistency), (0.20, clean), (0.15, adherence)]
    tool_ids = [t for t in ids if tasks[t]["has_tools"]]
    if tool_ids:
        comps.append((0.25, wmean(tool_ids, "self_verify_rate")))
    wsum_r = sum(wt for wt, _ in comps)
    reliability = 100 * sum(wt * v for wt, v in comps) / wsum_r
    efficiency = wmean(ids, "eff")
    return dict(correctness=correctness, reliability=reliability,
                efficiency=efficiency, capability=capability)

def composite(cat, weights=WEIGHTS):
    return sum(cat[k] * weights[k] for k in weights)

def bootstrap_ci(tasks, weights, B=2000, seed=12345):
    """Cluster bootstrap: resample whole clusters (not tasks) with replacement — tasks within a
    cluster are correlated, so a per-task bootstrap would understate the CI."""
    rng = random.Random(seed)
    clusters = {}
    for t in tasks:
        clusters.setdefault(cluster_of(t), []).append(t)
    ckeys = list(clusters)
    comps = []
    for _ in range(B):
        tmp = {}
        for k in range(len(ckeys)):
            c = rng.choice(ckeys)
            for t in clusters[c]:
                tmp["%s#%d" % (t, k)] = tasks[t]
        comps.append(composite(categories(tmp), weights))
    comps.sort()
    lo = comps[int(0.025 * B)]; hi = comps[int(0.975 * B)]
    return lo, hi

def paired_pvalue(tasksA, tasksB, B=10000, seed=999):
    """Two-sided paired sign-flip permutation test on per-cluster pass-rate differences over the
    tasks both harnesses ran (they share tasks and seeds, so the pairing is exact). Returns
    (mean_diff, p) or None if there is no overlap."""
    shared = sorted(set(tasksA) & set(tasksB))
    if not shared:
        return None
    clusters = {}
    for t in shared:
        clusters.setdefault(cluster_of(t), []).append(t)
    diffs = [statistics.mean(tasksA[t]["pass_rate"] - tasksB[t]["pass_rate"] for t in ts)
             for ts in clusters.values()]
    obs = statistics.mean(diffs)
    if all(d == 0 for d in diffs):
        return obs, 1.0
    rng = random.Random(seed)
    hits = 0
    for _ in range(B):
        s = statistics.mean(d if rng.random() < 0.5 else -d for d in diffs)
        if abs(s) >= abs(obs) - 1e-12:
            hits += 1
    return obs, hits / B

def main():
    res = os.path.join(HB, "out", "results.csv")
    if not os.path.exists(res):
        print("no results yet at out/results.csv — run the matrix first"); sys.exit(1)
    rows = load(res)
    by_h = {}
    for r in rows:
        by_h.setdefault(r["harness"], {}).setdefault(r["task"], []).append(r)

    out = {"weights": WEIGHTS, "harnesses": {}}
    raw = {}   # unrounded per-task aggregates, for paired tests
    for h, tdict in by_h.items():
        tasks = {t: task_aggregate(reps) for t, reps in tdict.items()}
        raw[h] = tasks
        cat = categories(tasks)
        comp = composite(cat)
        lo, hi = bootstrap_ci(tasks, WEIGHTS)
        w = weights_for(list(tasks))
        tw = sum(w.values()) or 1
        out["harnesses"][h] = {
            "categories": {k: round(v, 1) for k, v in cat.items()},
            "composite": round(comp, 1), "ci95": [round(lo, 1), round(hi, 1)],
            "n_tasks": len(tasks),
            "pass_at_k": round(100 * sum(w[t] * tasks[t]["pass_any"] for t in tasks) / tw, 1),
            "pass_pow_k": round(100 * sum(w[t] * tasks[t]["pass_all"] for t in tasks) / tw, 1),
            "tasks": {t: {kk: (round(vv, 2) if isinstance(vv, float) else vv)
                          for kk, vv in a.items()} for t, a in tasks.items()},
        }
    # paired sign-flip permutation tests between every harness pair (shared tasks + seeds)
    out["paired"] = {}
    hs = sorted(raw)
    for i in range(len(hs)):
        for j in range(i + 1, len(hs)):
            r = paired_pvalue(raw[hs[i]], raw[hs[j]])
            if r:
                out["paired"]["%s vs %s" % (hs[i], hs[j])] = {
                    "pass_rate_diff": round(r[0], 3), "p": round(r[1], 4)}
    os.makedirs(os.path.join(HB, "out"), exist_ok=True)
    json.dump(out, open(os.path.join(HB, "out", "scores.json"), "w", encoding="utf-8"), indent=2)
    render(out)
    print("wrote out/scores.json and out/LEADERBOARD.md")

def render(out):
    H = out["harnesses"]
    order = sorted(H, key=lambda h: -H[h]["composite"])
    lines = []
    lines.append("# HarnessBench Leaderboard\n")
    lines.append("Category scores are 0-100 (absolute anchors). OVERALL = "
                 "0.35·Correctness + 0.25·Reliability + 0.20·Efficiency + 0.20·Capability, "
                 "with a 95% bootstrap CI over tasks.\n")
    lines.append("| # | Harness | Correct | Reliab | Effic | Capab | **OVERALL** | 95% CI | pass@k | pass^k |")
    lines.append("|---|---------|--------:|-------:|------:|------:|------------:|:------:|------:|------:|")
    any_fallback = False
    for i, h in enumerate(order, 1):
        c = H[h]["categories"]; comp = H[h]["composite"]; ci = H[h]["ci95"]
        # flag harnesses whose Efficiency used the wall-clock fallback for any task: that mode
        # is not commensurable with the overhead-ratio mode, so the number carries an asterisk
        fb = any(a.get("eff_mode") == "wallclock" for a in H[h]["tasks"].values())
        any_fallback = any_fallback or fb
        lines.append("| %d | %s | %.0f | %.0f | %.0f%s | %.0f | **%.1f** | %.0f–%.0f | %.0f | %.0f |" % (
            i, h, c["correctness"], c["reliability"], c["efficiency"], "\\*" if fb else "",
            c["capability"], comp, ci[0], ci[1], H[h]["pass_at_k"], H[h]["pass_pow_k"]))
    if any_fallback:
        lines.append("\n\\* Efficiency used the wall-clock fallback for one or more tasks "
                     "(no token instrumentation) — not directly comparable to overhead-ratio scores.")
    if out.get("paired"):
        lines.append("\n## Paired comparisons (per-cluster pass rate, sign-flip permutation test)\n")
        lines.append("| Pair | mean Δpass | p (two-sided) |")
        lines.append("|------|-----------:|--------------:|")
        for pair, d in sorted(out["paired"].items()):
            lines.append("| %s | %+.3f | %.4f |" % (pair, d["pass_rate_diff"], d["p"]))
    lines.append("\n## Per-task pass rate (by difficulty)\n")
    all_tasks = sorted({t for h in H for t in H[h]["tasks"]},
                       key=lambda t: (-next(H[h]["tasks"][t]["difficulty"] for h in H if t in H[h]["tasks"]), t))
    head = "| Task | d | " + " | ".join(order) + " |"
    lines.append(head)
    lines.append("|------|---|" + "|".join(["---"] * len(order)) + "|")
    for t in all_tasks:
        d = next(H[h]["tasks"][t]["difficulty"] for h in H if t in H[h]["tasks"])
        cells = []
        for h in order:
            a = H[h]["tasks"].get(t)
            cells.append("%.0f%%" % (100 * a["pass_rate"]) if a else "—")
        lines.append("| %s | %d | %s |" % (t, int(d), " | ".join(cells)))
    open(os.path.join(HB, "out", "LEADERBOARD.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")

if __name__ == "__main__":
    main()
