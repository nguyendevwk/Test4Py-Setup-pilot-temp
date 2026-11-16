> **Current development protocol v4:** [MULTITARGET_V4.md](MULTITARGET_V4.md). Four-arm SLM grounding screen; v3 results remain historical evidence.

# Council multi-target: engineering screen v3

This is a development screen for `council_multitarget.py`, not the upstream
Test4Py experiment. A successful screen does not prove assertion correctness,
mutation efficacy, generalization or improvement over the paper. Do not pool v3
with v2 or the previous EVALUATION_OUTPUT. Full research evaluation still needs
matched upstream controls, held-out targets and reviewed fault-detection metrics.

## Fixed small plan

- `docstring_parser_parse`: parser input/API handling.
- `codetiming_timer`: constructor and start/stop lifecycle.
- Source pins: docstring_parser `a8e2a3ba5a4cdd906830735cb41a6a22c9346bf4`;
  codetiming `e51e4c3a50a395e301c33013cd048182f961f369`. These form a NEW cohort,
  not a replay of the historical ZIP, whose source SHAs were not recorded.
- Arms: baseline, ranked, verified. One attempt per arm; six planned outcomes.
- Seed 42; temperature 0.7; top_p 0.95; 2048 output tokens per call.
- Coder Qwen2.5-Coder-7B-Instruct on GPU 0; Critic Qwen3-4B-Instruct-2507 on
  GPU 1. Both NF4. One repair maximum for a failed suite or extraction failure.
- All arms receive the same runtime API inventory and source. baseline is Council
  without setup. ranked uses a manually curated hint. verified checks execution of
  that hint in the checkout; it does NOT verify target invocation/preconditions.
- No test pruning, no seed selection, no automatic retries of unfavorable results,
  no automatic full experiment. Import repairs preserve tests/checks. Changed
  assertion expressions require review even when the resulting suite passes.

This checks two previously failing targets, not a representative benchmark. A
single attempt is intentional for engineering diagnosis, not statistical inference.
No runtime estimate is promised; six previous attempts took about 19 minutes before
model load. Record actual time and reserve time for model download/load.

## Run locally (no model/network)

Use Python with pytest, pytest-json-report and coverage installed:

```bash
python -m unittest discover -s tests -v
python council_multitarget.py --mock --output /tmp/council-v3-mock
```

Mock exercises queue/artifact writing only: metrics are NA and readiness is false.
Offline tests use a clearly labeled temporary toy project. They test real pytest,
coverage, collection failures, timeout/process handling, mixed-suite repair, raw
output retention, assertion/test removal gates, source modification detection,
replay and malformed extraction. Toy results are not research measurements.

## Kaggle Dual T4

For a single-file upload with Git clone, open
`notebooks/kaggle_git_clone_smoke_v3.ipynb`. It clones pinned base commit
`e86fab21d11494277d5029ff9d1c673e5c9927b0` then applies a SHA-256-checked
embedded overlay of the current runner, helper, regression tests and their reference
notebook. No source ZIP is needed; fixes have not been pushed to the remote.
`notebook-source.json` records the base and overlay hashes in the final archive.

Alternatively open `notebooks/kaggle_multitarget_smoke_v3.ipynb`. Use the updated source bundle,
not an old GitHub checkout. Enable Internet and T4 x2. The notebook uses the modern
bootstrap from the repository, then installs the optional NF4 runtime packages
before preflight. Torch/CUDA are inherited from Kaggle. Versions are recorded;
retain the environment manifest and resolved model SHAs for replay.

Equivalent commands after environment setup (use the same interpreter throughout):

```bash
python -m unittest discover -s tests -p test_multitarget.py -v
python council_multitarget.py --prepare-only --output /kaggle/working/SMOKE_PREFLIGHT
python council_multitarget.py --prepared /kaggle/working/SMOKE_PREFLIGHT/preflight.json --output /kaggle/working/SMOKE_V3
```

Every command reserves a fresh output; if the path exists, a sibling is created.
Use the actual `Reports:` path, not the old directory. The notebook allocates unique
paths in advance. Preparation records resolved target commits/hashes and checks
API imports come from those checkouts, not an installed package. The run refuses
changed/unready prepared sources. No dependency is installed inside a model run.

## Readiness and failure handling

Each real sample runs in its own product copy. The runner saves every prompt/raw
answer, selected code, extraction errors, repair audit, setup probe, pytest JSON,
process output, coverage counts and sample result. A failing sample does not stop
later planned samples. Model/preflight failure creates six explicit failure rows.
A timeout kills the subprocess group. Isolation is not a security sandbox.

No stdout regex is used to invent nodeids/counts. Collection failure has zero
executed nodes and coverage NA. Coverage is measured only for all-pass suites;
line = covered_lines/num_statements, branch = covered_branches/num_branches,
with no branches -> NA. These are MODULE metrics, not target-only metrics.
Accepted suites are replayed in a fresh process and coverage/node sets compared.

`readiness.json` is a conservative automated gate. Every planned sample must have:

- An all-pass nonempty suite without pruning, plus a stable replay.
- Positive measured module coverage (branch may be NA for branchless code).
- No source modification, unresolved setup, hollow syntax or literal-true assertion.
- No repair assertion changes pending semantic review.

The gate always retains `semantic_review_required: true`: inspect assertions,
target reach and whether the tests exercise meaningful scenarios. A green gate is
necessary engineering evidence, not sufficient evidence for a full study.
A red gate means inspect artifacts; do not rerun/select seeds until it turns green.
Fixes based on this screen require a new protocol/source hash and new screen run;
keep previous failures. These development targets cannot become held-out evidence.

Runner exit 2 means failed readiness/preflight; summary/ZIP are still produced for
model runs. Read artifacts before deciding the next action. A human must review
source, assertions, fault metrics and research design before the full experiment.
