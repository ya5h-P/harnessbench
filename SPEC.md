# HarnessBench — specification (v1)

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
  by fixed anchors `R≈1→100, 2→84, 3→68, 5→45, 8→22, 12→8`. If a harness doesn't report output
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
- Harness pairs share tasks *and* seeds, so a **paired sign-flip permutation test** on per-cluster
  pass-rate differences is reported alongside the leaderboard (don't trust a ranking whose p is large).
- One **warmup** run per harness is discarded (cold model/prompt cache).
- Run order is **shuffled/interleaved** to spread thermal drift; the tok/s probe time-series
  (`out/tokps.csv`) records drift.

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
150 tasks across difficulty 1–5 (d1: 5, d2: 27, d3: 61, d4: 42, d5: 15) in three groups:
- **52 hand-authored tasks** (21 from real GitHub repos — papergen, littleutils, first, boltons —
  pinned + vendored under `tasks/repos/`; the rest controlled synthetic).
- **98 generated harness-load tasks** in 11 parameterized families (`tasks/_authoring/`
  `generate_families.py`). These hold per-step model difficulty LOW and scale the *orchestration*
  load — the thing that differs between harnesses: `needle` (find a described function among
  5→200 files), `bigfile` (precise edit in a 60→1200-function file), `multiedit` (rename across
  3→18 call sites, no stragglers), `manyfix` (6→28 trivial fixes, all required), `chain` (execute
  a 2→5-step pipeline, sometimes fixing a step), `weirdfs` (hostile paths + decoys), `readdocs`
  (constants buried in long docs), `logdig` (answers from 3k→40k-line logs), `testfix`
  (run-test-iterate with hidden supersets), `editfid` (byte-fidelity edits: tabs, CRLF, minified
  JSON, long lines, regex escapes), `exactout` (exact output contracts).
- Every family is a statistical **cluster** (see Scoring math), so family size adds difficulty
  resolution without adding leaderboard weight.

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
- **`out_tokens` is self-reported** from each harness's own log format; cross-harness token
  accounting has not been externally validated. The tok/s baseline probe uses a fixed generation
  whose speculative-decoding acceptance differs from real task content, so Efficiency carries
  normalization noise. Wall-clock-fallback Efficiency scores are asterisked in the leaderboard and
  are not commensurable with overhead-ratio scores.
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
