# Optional concise-output development screen

Policy: `single-test-v1`. This is a new development cohort, not a continuation
that overwrites the earlier measurements.

**Measured status: not recommended for application use.** On the fresh real
14B screen, the model produced complete multi-test answers which the one-test
rule rejected. After four such baseline and five improved rejections, the
development screen was stopped early. All four planned module results remain
incomplete/NA; the original evidence and operator-stop receipt are preserved in
`research/artifacts/nf4_14b_fresh_compact_execution_20261117.json`. This is a
failed transport constraint, not a measured 0% efficacy result. The reviewed
working subset is in `research/application/14b_genty_curated_20261117/README.md`.

The observed 4096/512-token 14B run sometimes generated many tests in one answer
and exhausted its output budget inside an unfinished code block. This screen
keeps the same weights, budgets and production frame, but applies a shared output
contract to both arms. Initial generation asks for one complete concise pytest
test per target function; supporting imports, fixtures and helpers remain
allowed. Static syntax/test-shape checks reject invalid answers without pruning
or rewriting them. Pytest collection remains authoritative. Repairs preserve
existing tests/checks and are not restricted to one test if a candidate already
contains several. Raw answers and cap failures are retained.

Only known test-generation and repair operations receive this contract.
Initialization, type decisions, summaries and retrieval queries do not. The
initialization cache can therefore be imported only after the existing exact
prompt/model/runtime/source checks. Changing the output contract does not
authorize changing model or context/output-token budgets under old calibration.

The baseline is **upstream with the shared output contract**, not identical
raw upstream prompting. The new plan records the policy and protocol suffix;
the report states this common intervention. A structural check does not certify
an oracle, target reach, useful fault detection or an improvement over the paper.

Use `notebooks/kaggle_14b_compact_retry.ipynb` in the existing prepared Kaggle
session after reviewing the previous run. It validates preparation and earlier
real memory evidence and imports exact greedy initialization only. It never
imports generated tests, repairs, pytest outcomes or mutation results. The new
output prefix is `UPSTREAM_NF4_COMPACT_`; earlier failures stay intact. It runs
only the four-trial small screen, never the larger pilot.

Build a self-contained current snapshot:

```bash
python scripts/build_paired_notebook.py
python scripts/build_resume_notebook.py \
  --reuse-initialization /kaggle/working/UPSTREAM_NF4_RESUME_20261116T174754946339Z \
  --test-output-contract single-test-v1
```

Local evidence before GPU adoption: 159 CPU tests passed. The exact 79-file
notebook overlay was applied to a fresh Git clone and passed 18 focused tests.
Both real pinned-upstream fixture arms also completed generation, pytest,
coverage/replay and mutation orchestration using scripted model/embedding
doubles. The fixtures exercise orchestration; actual backend output-contract
behavior is checked separately with fake tokenizer/model tests. These are
engineering checks, not real 14B quality results.

Fresh-session GPU memory calibration passed before generation. The subsequent
transport screen was stopped as described above; no larger run was launched.
`notebooks/kaggle_14b_fresh_compact.ipynb` is a historical reproduction notebook
for a new empty session. It embeds the audited initialization evidence, prepares
fresh environments and calibration, and waits for its job so Save Version can
retain outputs. Its existence does not recommend repeating the failed policy.
