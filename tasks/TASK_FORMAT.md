# HarnessBench task contract

Every task is a directory `tasks/<id>/` containing:

```
tasks/<id>/
  task.json        # metadata (see schema below)
  prompt.txt       # the exact instruction handed to the harness
  fixtures/        # files copied into the agent workdir BEFORE the run (what the agent sees)
  grade.py         # HIDDEN grader. contract: python grade.py <workdir> <gradedir>
  hidden/          # (optional) hidden files copied into <gradedir> only (superset tests, expected data)
  gen.py           # (optional) reseeded fixture generator: python gen.py <workdir> <gradedir> <seed>
  ref/             # reference SOLUTION applied over fixtures -> grader must PASS  (preflight)
  buggy/           # (optional) unsolved state -> grader must FAIL (preflight). default = fixtures/
```

## task.json schema
```json
{
  "id": "stack_debug",
  "domain": "debug-to-green",
  "difficulty": 3,                  // 1..5 ; also the Correctness/Capability weight
  "timeout_s": 480,                 // hard wall-clock cap -> TIMEOUT failure class
  "reseed": false,                  // true => gen.py is invoked with a fresh seed each repeat
  "grader_token": "STACK OK",       // grade.py prints this exact line on success (sanity)
  "notes": "free text"
}
```

## Grader contract (uniform, language-agnostic to the harness)
- Invoked as: `python grade.py <workdir> <gradedir>`
  - `<workdir>`  = the agent's working directory (its produced artifacts).
  - `<gradedir>` = a clean directory holding hidden tests / expected values (agent never saw it).
- MUST print a single summary line and exit **0 on PASS**, **non-zero on FAIL**.
- MUST execute the produced artifact (never trust prose). MUST be deterministic given the fixtures.
- MUST normalize CRLF/trailing-whitespace when comparing text.

## Runner pipeline (run_one.sh) — per (task, harness, repeat, seed)
1. fresh `workdir/`; `gradedir/` is created but stays **empty during the run** (hidden files on
   disk would be readable from `../grade`). The initial setup materializes hidden outputs to a
   throwaway temp dir just to drive `gen.py`'s visible-fixture side.
2. if `gen.py`: `python gen.py workdir <tmp> <seed>` (writes visible fixture to workdir). else:
   copy `fixtures/*` -> workdir.
3. invoke the harness (via its adapter) with `prompt.txt`, cwd=workdir, hard timeout.
   `HB_TASKDIR` is exported only for the mock adapter — real harnesses never see task paths.
4. **materialize gradedir now** (same seed => identical hidden expected values) — this also means
   agent edits to fixture/test files are never trusted for grading.
5. `python grade.py workdir gradedir` -> failure class PASS/WRONG/CRASH/TIMEOUT/REFUSED
   (CRASH = nonzero harness exit; REFUSED = clean exit with an empty/near-empty log).
6. adapter parses harness logs -> tool calls, turns, output tokens, self_verify.
7. **integrity scan**: the harness log is grepped for task-dir/grade-dir access; hits are recorded
   in `out/flags.csv` for manual review.
8. append a row to `results.csv`.

## Preflight (preflight.sh) — discrimination guarantee, run by the author, no harness
For every task: apply `buggy/` (default fixtures) -> grader must FAIL; apply `ref/` -> grader must
PASS; if `reseed`, run twice with different seeds and confirm expected values differ. Any violation
blocks the task from the suite.
