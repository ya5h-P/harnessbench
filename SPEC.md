# HarnessBench — specification (v2)

A standardized, reproducible, hard-to-game benchmark for **coding-agent harnesses** (pi, opencode,
hermes, …) driving a single shared model. It measures the *harness*, not the model: any backing
model can be used, and tok/s normalization removes raw model speed from the Efficiency score.

## What it measures
Four category scores (0–100, absolute anchors) plus one composite:

| Category | Weight | What it captures |
|----------|:------:|------------------|
| **Correctness** | 35% | Difficulty-weighted pass rate (graders execute the produced artifact). |
| **Reliability** | 25% | Consistency (pass^k), self-verification, clean completion, instruction adherence. |
| **Efficiency** | 20% | Per-turn/token overhead, normalized by server tok/s (not raw model speed). |
| **Capability** | 20% | Difficulty-weighted pass rate on the hard subset (difficulty ≥ 4). |

**HBench Score** = 0.35·Correctness + 0.25·Reliability + 0.20·Efficiency + 0.20·Capability,
reported with a 95% bootstrap CI over tasks. All four categories are always published separately.
Weights live in `score.py` (`WEIGHTS`).

## Scoring math (absolute anchors)
Anchors are fixed, so adding a new harness never changes existing harnesses' scores.
- **Task clusters**: near-duplicate tasks (the littleutils_*/boltons_* single-function fixes) form
  clusters; every task is weighted 1/|cluster| in all means, so one repeated skill can't dominate.
  Non-clustered tasks are singletons (weight 1). Clusters are defined in `score.py`
  (`CLUSTER_PREFIXES`).
- **Correctness** = 100·Σ(difficulty·w·pass_rate)/Σ(difficulty·w) over all tasks (w = cluster weight).
- **Capability** = same, restricted to difficulty ≥ 4 tasks.
- **Reliability** = weighted blend of pass^k consistency (0.40), self-verification rate (0.25),
  clean-completion rate (0.20), instruction-adherence pass rate (0.15). If a harness exposes no tool
  instrumentation, the self-verification term is dropped and the remaining weights renormalize
  (so a partially-instrumented harness is not penalized with zeros).
- **Efficiency** = per-task overhead ratio R = wall_time ÷ (output_tokens ÷ tok/s_baseline), mapped
  by fixed anchors `R≈1→100, 2→84, 3→68, 5→45, 8→22, 12→8`. When the server exposes llama.cpp
  `/metrics`, both output_tokens and tok/s_baseline are measured server-side per run (counter
  deltas around the invoke — the run's actual requests at real context depth); otherwise
  output_tokens is harness-reported and tok/s comes from the synthetic probe. If neither yields
  tokens, a wall-clock fallback (`wall_s ÷ difficulty` vs fixed anchors) is used instead. R≈1 means
  "all time is generation" (ideal); high R means prompt/per-turn overhead.

## Failure taxonomy (not just pass/fail)
Each run is classified PASS / WRONG / CRASH / TIMEOUT / REFUSED. CRASH/TIMEOUT/REFUSED reduce the
clean-completion component of Reliability more than a clean WRONG answer. Every task has a hard
timeout (`task.json:timeout_s`).

## Statistical protocol
- **N repeats** per task (default 5; `--repeats`), each with a different seed.
- Per task, pass rate is the **mean** over repeats; wall-clock/token figures use the **median**.
  The CI is a **cluster bootstrap** over tasks (clusters resampled whole — tasks within a cluster
  are correlated, so a per-task bootstrap would understate the CI).
- **pass@k** (passed ≥1 of k = capability ceiling) and **pass^k** (passed all k = consistency) are
  both reported; their divergence is a signal.
- **Run-to-run stability (Kendall τ-b, report-only)**: mean pairwise τ-b between repeats, in two
  forms. **τ-out** on per-task binary pass vectors — high means the same tasks fail every run
  (systematic weakness), low means failures wander between runs (sampling noise); it tells you
  *which kind* of inconsistency the pass@k/pass^k gap is made of. **τ-eff** on per-task wall-time
  rankings — how stable a task's cost is across runs. Neither enters the composite.
- Harness pairs share tasks *and* seeds, so a **paired sign-flip permutation test** on per-cluster
  pass-rate differences is reported alongside the leaderboard (don't trust a ranking whose p is large).
- One **warmup** run per harness is discarded (cold model/prompt cache).
- Run order is **shuffled/interleaved** to spread thermal drift; the per-run server measurements
  (`out/server_usage.csv`, or the probe time-series `out/tokps.csv` in fallback mode) record drift.

## Anti-gaming guarantees
- **Hidden graders**: the agent never sees `grade.py`. Agent-visible tests are graded against a
  **hidden superset**, so "make the shown test pass" is insufficient.
- **No hidden files on disk during the run**: the gradedir is *empty* while the agent runs and is
  materialized (deterministically from the run's seed) only after the harness exits, so reading
  `../grade` yields nothing. `HB_TASKDIR` (which points at `grade.py`/`hidden/`/`ref/`) is exported
  only to the mock adapter, never to a real harness.
- **Integrity scan**: after each run the harness log is scanned for accesses to the task dir or a
  grade dir; hits are recorded in `out/flags.csv` and warned on the console for manual review.
- **Fresh-copy grading**: hidden test files are re-stamped after the run, so editing fixture/test
  files doesn't help.
- **Un-hardcodable answers**: reseeded tasks regenerate fixtures/cases every repeat; expected values
  are computed by the grader from the actual fixture, never in the prompt.
- **Execution-grounded**: graders run the produced code; prose claims are ignored.
- **preflight.sh** guarantees every grader FAILS the unsolved state and PASSES a reference solution,
  and that reseeds change the expected value — any violation blocks the task.

## Fairness across harnesses
- Identical backing model/endpoint/sampling for all harnesses (pin + record: model id, server flags).
- Each harness runs in its documented non-interactive auto-approve mode (a harness that stalls on a
  prompt → REFUSED). Launch quirks are encoded in the adapter (e.g. opencode is launched as the exe
  directly — the PowerShell `| Out-String` wrapper hangs at init on Windows).
- A harness's own config (context window, temperature) is part of "the harness as shipped" — recorded,
  not equalized.

## Task suite
200 tasks across difficulty 1–5 (d1: 4, d2: 16, d3: 50, d4: 80, d5: 50), deliberately
top-heavy: d4 is where harnesses separate, so 65% of the suite is d4–d5. Two groups:
- **67 hand-authored tasks** (21 from real GitHub repos — papergen, littleutils, first, boltons —
  pinned + vendored under `tasks/repos/`; the rest controlled synthetic). Includes the v2
  hand-authored tail generated by `tasks/_authoring/gen_authored.py` (14 performance tasks with
  machine-independent relative-speedup gates), `gen_security.py` (10 security-critical tasks:
  SSRF allowlist, HTML/SQL/command injection, mass-assignment, unsafe deserialization, auth-before-
  mutation, Zip Slip, ReDoS, path traversal — each graded by a hidden probe that must block the
  attack *and* preserve legitimate behavior), and `gen_refactor.py` (3 refactor-under-constraints
  tasks: split-under-line-cap with a frozen public API, keyword-only signature codemod, and a
  stateful vendored-dependency removal that also requires a migration-notes artifact).
- **133 generated harness-load tasks** in 11 parameterized families (`tasks/_authoring/`
  `generate_families.py`). These hold per-step model difficulty LOW and scale the *orchestration*
  load — the thing that differs between harnesses: `needle` (find a described function among
  8→320 files), `bigfile` (precise edit in a 90→2000-function file), `multiedit` (rename across
  3→28 call sites, no stragglers), `manyfix` (8→40 trivial fixes, all required), `chain` (execute
  a 3→7-step pipeline, sometimes fixing 1–2 steps), `weirdfs` (hostile paths + up to 56 decoys),
  `readdocs` (constants buried in up to 10 docs, with deprecated-value traps), `logdig` (answers
  from 4k→150k-line logs), `testfix` (run-test-iterate with hidden supersets), `editfid`
  (byte-fidelity edits: tabs, CRLF, Latin-1, minified JSON, long lines, regex escapes, fixed-width
  columns), `exactout` (exact output contracts).
- Every family is a statistical **cluster** (see Scoring math), so family size adds difficulty
  resolution without adding leaderboard weight.

### v2 task metadata (report-only; does not affect scoring)
Three optional `task.json` fields (backward-compatible; v1 tasks default sensibly):
- **`capability`** — the harness mechanism a failure implicates (search-navigation, cross-file
  consistency, edit-fidelity, sustained-coverage, multi-step-execution, context-grounding,
  injection-safety, …). A task whose failures implicate *no* harness capability is tagged
  `"floor"` and must stay d1–2 — **preflight rejects a d≥3 task tagged `floor`** (attributable-
  failure rule).
- **`tier`** — `"variance"` (near the capability frontier; drives the pass^k signal) or
  `"systematic"` (deliberately beyond it — e.g. needle at 320 files — driving the pass@k signal).
  The suite is 142 variance / 58 systematic. Systematic d5 tasks are capped at the d4 timeout
  (they are expected to fail; a correct solve is fast).
- **`stateful`** — a later step depends on an artifact/decision from an earlier step in the same
  session (tests context retention). 10 tasks are stateful (the d4/d5 `chain` pipelines and the
  vendored-dependency-removal refactor).

Retired v1 tasks live under `tasks/_archive/` (excluded from the matrix and scoring — the runner
and preflight glob only the direct children of `tasks/`); see that folder's README for the
selection rationale. Nothing is deleted, so v1 remains reproducible.

See `tasks/TASK_FORMAT.md` for the task/grader contract and `tasks/repos/REAL_REPOS.md` for the
real-repo curation protocol + provenance.

Difficulty rubric: 1 trivial · 2 single-function/CLI · 3 multi-file/refactor/stateful · 4 real-repo
cross-module bug / perf / concurrency / codemod / test-authoring / heavy orchestration · 5
multi-defect / security+gate / large codemod / marathon orchestration (100+ files, 20+ edits,
multi-step pipelines).

## Known limitations (read before citing results)
- **Single backing model per leaderboard.** Pass rates are harness×model interactions; a ranking
  produced on one model may not transfer to another. To claim a harness ranking generalizes,
  replicate on ≥2 models and check rank stability.
- **Repeats measure sampling variance, not robustness, for non-reseeded tasks.** Only reseeded
  tasks change inputs across repeats; elsewhere a harness that ships temperature 0 gets a perfect
  pass^k by determinism. "Harness as shipped" is the design stance — but read pass^k accordingly.
- **Token accounting depends on the serving stack.** With llama.cpp `/metrics` enabled,
  `out_tokens` and tok/s are measured server-side per run and are harness-neutral by construction.
  Without it, `out_tokens` is self-reported from each harness's log format (not externally
  validated across harnesses) and the synthetic tok/s probe uses a fixed generation whose
  speculative-decoding acceptance differs from real task content, so fallback-mode Efficiency
  carries normalization noise. Don't mix server-measured and probe-measured rows in one
  leaderboard (`src=` is recorded per run). Wall-clock-fallback Efficiency scores are asterisked
  in the leaderboard and are not commensurable with overhead-ratio scores.
- **Difficulty weights are author-assigned** ordinals used as ratio weights; re-run `score.py`
  with different `WEIGHTS`/difficulties to check sensitivity (results ship with the per-task table
  so readers can re-derive).

## Adding a harness
Write `adapters/<name>.sh` with two subcommands:
- `invoke <workdir> <promptfile> <outdir>` — run the harness non-interactively in `workdir`, write its
  log to `outdir` (return its exit code).
- `metrics <workdir> <outdir>` — print `toolcalls=N turns=N out_tokens=N self_verify=0|1 tools=...`
  parsed from the harness's logs/session store.
Then `bash run_matrix.sh --harness <name>`. No other code changes are needed.
