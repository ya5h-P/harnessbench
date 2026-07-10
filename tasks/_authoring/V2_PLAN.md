# HarnessBench v2 suite — expansion blueprint

Status: **proposed, awaiting sign-off before task generation.** Target 200 tasks (from 150).
Motivation: the v1 run showed d4 is where harnesses separate, yet v1 is bottom-heavy. This rebalances
toward the hard band and reorganizes by *harness capability under test* rather than by generator family.

## 1. Target distribution

### By difficulty (column margins)
| band | v1 | v1 % | v2 target | v2 % |
|------|---:|-----:|----------:|-----:|
| d1–2 (floor/sanity)      |  32 | 21% | **20** | 10% |
| d3 (moderate)            |  61 | 41% | **50** | 25% |
| d4 (hard — primary signal) | 42 | 28% | **80** | 40% |
| d5 (stress/tail)         |  15 | 10% | **50** | 25% |
| **total** | 150 | | **200** | |

### By task type (row margins)
| type | v2 count | % | covering families / tasks |
|------|---------:|--:|---------------------------|
| Multi-site edits (rename/refactor/codemod) | 50 | 25% | multiedit, editfid, api_codemod, *_refactor |
| Large-context navigation (find-in-N)       | 40 | 20% | needle, bigfile, weirdfs, logdig, readdocs |
| Multi-defect repair                        | 30 | 15% | manyfix, chain, multi_defect, duration_multidefect |
| Test-driven fix                            | 24 | 12% | testfix, test_authoring |
| Performance / concurrency                  | 20 | 10% | perf_*, wordfreq_perf, *_concurrency |
| Exact-output / format adherence (floor)    | 20 | 10% | exactout, greet_format, fizzbuzz, stats_cli |
| Security / correctness-critical            | 16 |  8% | safe_eval, sql_safe, path_security, + new |

### Joint grid (type × difficulty) — the authoring target, margins verified
| type \ d | d1–2 | d3 | d4 | d5 | Σ |
|----------|-----:|---:|---:|---:|--:|
| Multi-site edits      | 2 | 12 | 24 | 12 | 50 |
| Large-context nav     | 6 | 10 | 16 |  8 | 40 |
| Multi-defect repair   | 0 |  6 | 14 | 10 | 30 |
| Test-driven fix       | 2 |  6 | 12 |  4 | 24 |
| Perf / concurrency    | 0 |  4 | 10 |  6 | 20 |
| Exact-output (floor)  |10 |  8 |  2 |  0 | 20 |
| Security-critical     | 0 |  4 |  2 | 10 | 16 |
| **Σ** | **20** | **50** | **80** | **50** | **200** |

> Authoring note: the Security d5=10 and Perf/concurrency cells are the most hand-authoring-intensive.
> During authoring these may drop a difficulty tier, compensated 1-for-1 by exact-output/navigation
> floor tasks, **without changing the column margins** (the d1–2/d3/d4/d5 totals are the hard constraint;
> the type split is a target with ±2 tolerance per cell).

## 2. Two design rules (from the request)

**Rule 1 — attributable failure.** Every task's dominant failure mode must trace to a *harness*
capability (search over N files, edit fidelity, multi-step tool execution, sustained coverage,
context compression, instruction adherence), **not** model intelligence. If the author can't name the
harness capability a failure would implicate, the task is a *floor* task and lives in d1–2 (capped at
10% of the suite). Concretely, each new task's `task.json` gains a `capability` field naming the
mechanism under test; preflight rejects a d≥3 task whose `capability` is `"floor"`.

**Rule 2 — variance vs systematic tier.** Each hard family is split into two tiers, tagged in
`task.json` as `tier: "variance" | "systematic"`:
- **variance tier** — solvable but sits near the capability frontier (small/medium parameter): drives
  the pass^k signal (flaky, seed-dependent). ~half of each family's d4/d5 members.
- **systematic tier** — genuinely beyond the current frontier (large parameter): drives the pass@k
  signal (fails most/all seeds for a reason, not for luck). The other half.
`score.py` (future, report-only) can then break pass@k/pass^k down by tier — turning today's
"32% of tasks flip" observation into a designed, measurable axis instead of an emergent one.

## 3. What changes, mechanically

### 3a. Generator family plan rewrites (`generate_families.py`)
The templated families are the cheap, preflight-safe source of d4/d5 bulk. Each family's `plan` list
is rewritten to shift mass into d4/d5 and tag tiers. Proposed new plans (param = existing knob:
needle=#files, bigfile=#funcs, multiedit=#call-sites, manyfix=#bugs, weirdfs=#decoys, chain=#steps):

| family | v1 plan (d-tally) | v2 plan (d-tally) | Δ tasks |
|--------|-------------------|-------------------|--------:|
| needle    | d2×2 d3×3 d4×3 d5×2 (10) | d2×1 d3×2 d4×5 d5×4 (12) | +2 |
| bigfile   | d2×2 d3×3 d4×3 d5×2 (10) | d2×1 d3×2 d4×5 d5×4 (12) | +2 |
| weirdfs   | d2×2 d3×3 d4×3     (8)   | d2×1 d3×2 d4×5 d5×3 (11) | +3 |
| multiedit | d3×3 d4×4 d5×3     (10)  | d3×3 d4×8 d5×5     (16)  | +6 |
| manyfix   | d3×3 d4×4 d5×3     (10)  | d3×2 d4×6 d5×5     (13)  | +3 |
| chain     | d2×2 d3×3 d4×3 d5×2 (10)  | d2×0 d3×2 d4×5 d5×4 (11) | +1 |
| testfix   | d2×3 d3×3 d4×2     (8)   | d2×1 d3×3 d4×6 d5×2 (12) | +4 |
| editfid   | d2×3 d3×3 d4×2     (8)   | d2×1 d3×3 d4×6 d5×2 (12) | +4 |
| logdig    | d2-heavy (10)           | d2×2 d3×3 d4×4 d5×2 (11) | +1 |
| readdocs  | d2×2 d3×3 d4×3     (8)   | d2×1 d3×3 d4×4 d5×3 (11) | +3 |
| exactout  | d1×3 d2×3 d3×2     (8)   | d1×3 d2×5 d3×4     (12)  | +4 |
| **Σ generated** | **98** | **~133** | **+33** |

Each new d4/d5 member also needs a *systematic-tier* variant beyond the current top parameter (e.g.
needle at 260/320 files, bigfile at 1600/2000 funcs, multiedit at 22/26 sites, manyfix at 32/36 bugs)
— these are the tasks expected to fail most seeds *systematically*, which the v1 suite lacked (its d5
marathons mostly hit 100%, giving pass@k no headroom).

### 3b. Hand-authored new tasks (~40)
Categories the generator can't template well, authored individually against TASK_FORMAT.md +
preflight. Priority order (highest validity value first):
- **Perf/concurrency (need +~13):** more `*_concurrency` (lock ordering, ABA, lost-update, fairness),
  perf gates on real algorithmic hot-loops (n² → n log n with a hidden large-input timeout).
- **Security-critical (need +~10):** path traversal variants, SSRF-style URL allowlist, deserialization
  safety, auth-check-before-mutation, injection beyond sql_safe. These are the *correctness-critical*
  tail — a wrong answer must be gradeable as unsafe, not just unequal.
- **Stateful multi-turn carve-out (~10, pulled from the hard families above, not additive):** tasks
  whose step 2 depends on an artifact/decision from step 1, testing session memory / context
  compression directly. Mark `stateful: true`. These are the only tasks that isolate the
  compression-under-long-context capability.
- **Refactor-under-constraints (ME tail):** larger codemods with invariants (public API frozen, no
  behavior change, no new deps) verified by hidden tests.

### 3c. Archival (23 tasks off-leaderboard → `tasks/_archive/`)
To hit d1–2 ≤ 20 and d3 ≤ 50, retire the 12 lowest-value floor tasks and 11 lowest-value d3 tasks
(near-duplicates and the least-discriminating). Selection metric: keep the tasks with the best
discrimination history and cluster coverage; archive redundant members. Archived tasks stay
**runnable** (preflight + ad-hoc) but are excluded from the v2 matrix and scoring via a new
`tasks/_archive/` location the runner skips. v1 reproducibility preserved (nothing deleted).
Final selection list to be produced from the discrimination + v1 pass-rate data before archiving.

### 3d. Schema additions (`task.json`)
Three optional fields, all backward-compatible (v1 tasks default sensibly):
- `capability`: string naming the harness mechanism under test (Rule 1). Default derived from domain.
- `tier`: `"variance" | "systematic"` (Rule 2). Default `"variance"`.
- `stateful`: bool (carve-out). Default `false`.
`SPEC.md` + `TASK_FORMAT.md` updated to document all three. None affect scoring until a future
report-only breakdown consumes them (preserving the absolute-anchor guarantee).

## 4. Runtime & rollout impact
- 200 × 5 repeats = **1000 runs/harness ≈ 13 h** at the current ~48 s/run. Three-way interleaved ≈ 39 h.
- Preflight cost: every new/changed task must pass the buggy-fails / ref-passes discrimination gate,
  and reseeded tasks must show changed expected values. ~73 new preflight cases.
- Suggested order: (1) schema + docs, (2) generator plan rewrite + regenerate + preflight the
  templated bulk, (3) hand-author perf/security/stateful, (4) archival wiring + final selection,
  (5) full preflight, (6) dry mock-matrix run, (7) real run.

## 5. Open decisions for sign-off
1. The type-split ±2 tolerance vs the hard difficulty margins — confirm difficulty margins win.
2. Archive selection metric — discrimination history vs pure difficulty pruning (proposed: former).
3. Whether the systematic-tier d5 tasks should have a *lower* per-task timeout (they're meant to fail;
   a 1500 s timeout on a task designed to fail wastes ~25 min/seed). Proposed: cap systematic-tier at
   the d4 timeout (900 s) since a correct solve, if it happens, is fast.
