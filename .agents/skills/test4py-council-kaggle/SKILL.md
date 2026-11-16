---
name: test4py-council-kaggle
description: Operational checks for Test4Py Council on Kaggle Dual T4; distinguish engineering screens from confirmatory experiments.
---

# Test4Py Council on Kaggle

## Scope and precedence

User instructions take precedence. Follow repository source and measured artifacts;
old runbooks and example campaign scripts do not establish readiness or efficacy.
Use `docs/MULTITARGET_V4.md` for the repaired multi-target development screen.
Use `docs/COUNCIL_V2.md` for the separate PyCG case study.
Council baseline is Council without setup, not upstream Test4Py (`run.py`/`worker.py`).
Never automatically launch a full campaign after a smoke run.

## Environment

Use a Python notebook cell with `subprocess.run(..., check=True)` and explicit cwd.
Keep Kaggle's CUDA Torch. Use an isolated environment and record resolved versions.
Coder and Critic can use separate T4 GPUs with NF4. Verify actual GPU count, model
revision, quantization and peak memory; do not infer memory safety from empty_cache.
Two T4s do not combine into one VRAM pool. Record load failures and OOMs.
Preserve output directories; use fresh paths and keep failure artifacts/archives.
Do not reset a checkout destructively to update it; use fast-forward or a fresh clone.

## Engineering screen

Run offline regression checks first, then dependency/import/setup preflight before
loading models. The small default screen has two targets, four arms, one attempt
per arm. It checks implementation, not statistical significance. Preserve all eight
planned outcomes, including model/extraction/collection/timeout failures.
Save full prompts, raw answers, extracted versions, probe logs, pytest JSON,
coverage counts, revisions, hashes and timing. Mock results have no efficacy metrics.

The multi-target runner currently uses curated setup hints. `ranked` means an
unprobed hint, not an automatically ranked candidate pool. `grounded` adds bounded production dependencies. `verified` witnesses target
function entry/normal completion, or constructor entry for a class. A class witness
is not a guarantee of method preconditions or oracle correctness.
A subprocess is process isolation, not a security sandbox.

## Integrity and interpretation

Do not drop failed tests, targets or seeds to improve a headline score. If tests
are recovered by filtering, report pre/post results and retention separately.
Do not weaken assertions to make tests pass. Preserve every revision and flag
changed assertions for review; syntactic gates cannot prove semantic preservation.
Report collection errors separately from executed test nodes. Missing coverage is
NA, measured zero stays zero, and no branches means branch coverage NA.
Use covered_lines/num_statements for line coverage and covered_branches/num_branches
for branch coverage. Always identify module vs target coverage.
A passing suite does not prove oracle correctness; require independent assertion
review and mutation/real-fault evaluation for research efficacy claims.

## Research design

Pre-register targets, source/model SHAs, seeds, budgets, metrics and exclusions.
Separate development targets from held-out projects. Multiple stochastic attempts
on one function are not independent targets. N=10/15 and temperature=0.7 do not
guarantee significance or justify a prescribed p-value. Choose statistical methods
for paired, clustered observations and report effect sizes and uncertainty.
Compare upstream on matched targets/budgets before claiming improvement over Test4Py;
never compare incompatible published aggregates to local screen results.
