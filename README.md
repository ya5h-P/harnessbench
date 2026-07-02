# HarnessBench

**Benchmark the coding-agent harness, not the model.**

Everyone benchmarks models. But if you run a local model, you've probably noticed that *which
agent CLI you wrap around it* changes the results just as much — one harness nails a task that
another fumbles, with the exact same weights behind both. HarnessBench measures that difference.

Point two or more coding-agent harnesses (pi, opencode, hermes, aider, your own…) at the **same
model endpoint**, run the same 150 tasks through each, and get an honest leaderboard:

```
| # | Harness  | Correct | Reliab | Effic | Capab | OVERALL  | 95% CI | pass@k | pass^k |
|---|----------|--------:|-------:|------:|------:|---------:|:------:|-------:|-------:|
| 1 | pi       |      96 |     98 |    96 |    92 | **95.5** | 87–100 |     97 |     97 |
| 2 | yourtool |       ? |      ? |     ? |     ? |    **?** |    ?   |      ? |      ? |
```

It's designed for exactly the setup most local-LLM tinkerers have: one machine, one
single-concurrency endpoint (llama.cpp, ollama, vLLM…), and curiosity about which harness
actually earns its keep on *your* hardware. Runs are resumable, so it's fine to kick it off
and walk away.

## What makes it trustworthy

- **Hidden, execution-grounded graders.** Every task is graded by running the produced code
  against hidden tests. The grade directory is *empty* while the agent works, agent-visible
  tests are a subset of the hidden ones, and the harness log is scanned for any attempt to
  peek. Prose claims count for nothing; only working artifacts pass.
- **A discrimination guarantee.** `engine/preflight.sh` proves every one of the 150 graders
  fails the unsolved state and passes a reference solution — before any model is involved.
- **Honest statistics.** Templated task families are treated as clusters (one skill can't
  dominate the score), the confidence interval is a cluster bootstrap, and harness pairs get a
  paired permutation test so you know whether a ranking gap is real or noise.
- **Harness-focused tasks.** 98 of the 150 tasks deliberately keep the *thinking* easy and
  scale the *orchestration*: find one function among 200 files, edit line 4,000 of a huge file,
  rename a symbol across 18 call sites, fix 28 trivial bugs without missing one, compute an
  answer from a 40k-line log. That's the stuff that separates harnesses.

See [SPEC.md](SPEC.md) for the full methodology, scoring math, and known limitations.

## Requirements

| | Windows | Linux / macOS |
|---|---|---|
| Shell | **Git Bash** (comes with [Git for Windows](https://gitforwindows.org/)) | bash (built in) |
| Python | 3.9+ on PATH | 3.9+ (`python3` is fine — see `HB_PYTHON`) |
| Other | `curl` (included in Git Bash) | `curl`, coreutils (`timeout`) |
| Model server | any OpenAI-compatible chat endpoint (llama.cpp `llama-server`, ollama, vLLM, …) | same |

And, of course, the harness CLIs you want to compare, each installed and configured to talk to
your endpoint.

## Try it in 60 seconds (no model needed)

The built-in `mock` harness plays a perfect agent, so you can verify the whole pipeline works
on your machine before spending any GPU time:

```bash
# 1. every grader must discriminate: "buggy rc=1, ref rc=0" for all 150 tasks
bash engine/preflight.sh

# 2. dry-run the pipeline end to end
bash run_one.sh mock fizzbuzz 1 1001 noprobe
bash run_one.sh mock chain_03 1 1001 noprobe

# 3. score it
python score.py        # Linux: HB_PYTHON=python3 python3 score.py
cat out/LEADERBOARD.md
```

If all of that works, you're ready for the real thing. (Delete the mock rows from
`out/results.csv` before a real run, or just delete `out/` entirely.)

## Configure for your machine

Everything is an environment variable — no config files to edit:

```bash
export HB_PYTHON=python3                                        # Linux, if `python` isn't a thing
export HB_ENDPOINT=http://localhost:8000/v1/chat/completions    # your server (tok/s probe)
export HB_MODEL=your-model-name                                 # model id your server expects

# tell the adapters where the harness CLIs live (examples):
export PI_NODE=/usr/bin/node PI_CLI=~/node_modules/@earendil-works/pi-coding-agent/dist/cli.js
export OPENCODE_EXE=~/.local/bin/opencode  OPENCODE_MODEL=llama.cpp/your-model-name
export HERMES_EXE=~/.local/bin/hermes
```

**Windows:** run everything from **Git Bash**, and use `/c/Users/you/...`-style paths in the
variables above. One hard-won tip is already baked in: opencode is launched as the exe directly,
because its PowerShell wrapper hangs at init on Windows.

**Linux/macOS:** everything is plain bash + coreutils; just set `HB_PYTHON=python3` if your
distro doesn't ship a `python` alias.

## Run the benchmark

```bash
# quick directional run: 1 repeat of everything (a few hours per harness on a slow endpoint)
bash run_matrix.sh --harness pi,opencode --repeats 1

# publication-grade: 5 repeats, different seeds
bash run_matrix.sh --harness pi,opencode,hermes --repeats 5

# or start with a subset
bash run_matrix.sh --harness pi --tasks fizzbuzz,needle_03,logdig_01 --repeats 1
```

Good to know:

- **Sequential on purpose.** Local endpoints usually handle one request at a time, so the runner
  never parallelizes. Run order is shuffled to spread thermal drift fairly across harnesses.
- **Resumable.** `out/results.csv` is the checkpoint. Ctrl-C anytime (or crash — we've tested
  that the hard way); re-running skips completed rows and continues.
- **A tok/s probe** fires between runs into `out/tokps.csv`, so Efficiency scores are normalized
  by your server's actual speed — a faster GPU doesn't make a harness look smarter.
- Flags: `--repeats N`, `--tasks all|id,..`, `--harness a,b`, `--seed-base S`, `--no-warmup`,
  `--no-probe`.
- If a timed-out harness leaves a zombie process holding your endpoint (mostly a Windows thing),
  kill the stray `node`/`opencode`/`hermes` process and re-run — it resumes.

Then score and read:

```bash
python score.py
cat out/LEADERBOARD.md      # leaderboard + per-task table + paired significance tests
```

`out/scores.json` has the full per-task breakdown. To re-weight the composite, edit `WEIGHTS`
in `score.py` and re-run scoring — no need to re-run the matrix. If `out/flags.csv` exists,
read it: it lists runs where a harness's log mentioned grader paths (integrity review).

## What the scores mean

| Category | Weight | Question it answers |
|----------|:------:|---------------------|
| **Correctness** | 35% | Did it solve the tasks? (difficulty-weighted) |
| **Reliability** | 25% | Does it solve them *every time*? Does it verify its own work? Does it finish cleanly? |
| **Efficiency** | 20% | How much wall-clock overhead beyond raw generation time? |
| **Capability** | 20% | How does it do on the hard tail (difficulty ≥ 4)? |

`pass@k` vs `pass^k` is the fun one: a harness that sometimes brilliant, sometimes faceplants
shows a big gap between the two.

## Add your own harness (please do!)

One file. Drop `adapters/<name>.sh` with two subcommands:

```bash
# run the harness non-interactively in <workdir> on the prompt; log to <outdir>
invoke <workdir> <promptfile> <outdir>

# parse your harness's own logs into uniform metrics
metrics <workdir> <outdir>     # prints: toolcalls=N turns=N out_tokens=N self_verify=0|1 tools=a,b
```

Look at `adapters/pi.sh` (JSON log parsing) or `adapters/mock.sh` (smallest possible example).
Then `bash run_matrix.sh --harness yourname`. That's it — scoring picks it up automatically,
and absolute anchors mean adding your harness never changes anyone else's score.

## Add tasks

- **One-off task**: copy any `tasks/<id>/`, follow [tasks/TASK_FORMAT.md](tasks/TASK_FORMAT.md),
  then run `bash engine/preflight.sh <id>` until it reports `buggy rc=1, ref rc=0`.
- **The 98 templated tasks** are generated by `tasks/_authoring/generate_families.py`
  (idempotent, self-checking). Extend a family there rather than editing generated dirs.
- **Vendor a real repo**: `bash fetch_repos.sh <name> <url> <sha>`, then see
  `tasks/repos/REAL_REPOS.md`.

## Publishing your results

Comparability depends on context, so record alongside any leaderboard you share: harness
versions (`pi --version`, etc.), model id + quantization + server flags, OS, and
`python --version`. Two leaderboards are only comparable when the backing model and endpoint
match — a harness ranking measured on one model does not automatically transfer to another
(that caveat and others are spelled out in [SPEC.md](SPEC.md#known-limitations-read-before-citing-results)).

## Repo layout

```
SPEC.md              methodology & scoring math
tasks/               150 task dirs (task.json, prompt.txt, fixtures/, hidden grade.py, ref/)
tasks/_authoring/    generator for the 98 templated harness-load tasks (11 families)
tasks/repos/         vendored real-repo snapshots (pinned @SHA) + curation guide
adapters/            pi.sh, opencode.sh, hermes.sh, mock.sh (+ parsers) — add yours here
engine/              setup.py (workdir/gradedir builder), preflight.sh (discrimination check)
run_one.sh           one (harness,task,repeat): setup -> invoke -> grade -> metrics -> csv
run_matrix.sh        the full matrix (sequential, resumable, shuffled, warmup)
probe_tokps.sh       server tok/s probe (Efficiency normalization + drift tracking)
score.py             scoring -> out/scores.json + out/LEADERBOARD.md
out/                 your results (gitignored): results.csv, tokps.csv, flags.csv, leaderboard
```

## License

MIT (see [LICENSE](LICENSE)). The vendored repo snapshots under `tasks/repos/` keep their own
upstream licenses (MIT for papergen/littleutils/first, BSD for boltons) — see
`tasks/repos/REAL_REPOS.md` for provenance.
