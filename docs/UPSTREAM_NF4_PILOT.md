# Paired upstream Test4Py pilot on Kaggle T4 x2

Protocol: `test4py-nf4-paired-pilot-v1`. Both arms use the real upstream pipeline,
not Council. This is a resource-constrained adapted reproduction, not a reproduction
of published GPT-4o aggregate numbers or a representative sample of 183 modules.
No claim of improved accuracy is made until the paired GPU evidence is available.

## Scope and controlled interventions

Upstream commit: `3c8b45410545183a9a579a784ffefae722a158a6`.
Both arms run full production-package call-graph initialization, caller/callee
summaries, type inference, retrieval, selected-module generation, coverage feedback
and adaptive repair. Only generation is limited to selected modules. This fixes
the earlier worker's substring-based selected-file filtering that lost context.

Baseline: upstream reasoning and repair. Shared explicit runtime adapters:

- Qwen/Qwen2.5-Coder-14B-Instruct, immutable model SHA resolved before inference,
  NF4 double quantization, FP16 compute/nonquantized tensors, no FP16 fallback or
  implicit CPU/disk offload. Same model performs every role in both arms.
- Same local complete-block extraction/newline behavior, CPU BGE embedding at a
  resolved SHA, and defined empty-retrieval behavior and a safe missing-`tests` JSON reader that retains
  collection failure instead of crashing with KeyError. CPU device substitution is
  an in-memory AST patch of exactly one upstream assignment; checkout is unchanged.
- Same input/output/sequence caps (default 6144/1024/7168), per-worker timeout,
  pytest/scoring environment, and generation exceptions retained per function.
- Greedy initialization and an exact-prompt, model/config/source-keyed shared cache.
  Model-generated summaries remain unverified. Cache is NEVER used for generation,
  repair, test outcomes or mutants. Generation/repair seed is reset after init.
  Seeds 42/43 therefore measure stochastic generation conditional on a common
  deterministic initialization, not independent end-to-end summary replications.
  Cache locking prevents duplicate concurrent computation; bad cache data fails closed.

Improved adds:

- Strict declared-member compatibility on upstream type candidates, with runtime
  verification of the actual class module/signature. Dynamic members can be false
  negatives; every rejection/unknown is archived.
- Source-backed class declaration context replacing model-invented usage examples;
  bounded production dependencies in generation/repair. No observed expected values.
- Import/unshadowed-module-attribute validation before syntax repair; dynamic
  namespaces stay unknown. Improved repair prompts forbid copying actual outputs
  into expectations; baseline retains the original upstream prompts.
- Deterministic missing stdlib-module
  imports only, logged as interventions, not raw-model first-pass successes.
- Upstream repair budget remains; a final candidate that changes/removes assertion
  expressions is rejected for automatic improved credit and retained for review.
  Baseline reduction remains upstream behavior and is audited. This policy difference
  is part of the treatment; do not label all effects as type-inference improvements.

An independent AST audit does not prove semantic preservation or oracle accuracy.
Project-specific exceptions/expected values are not hardcoded into the algorithm.
Neither arm uses another model, hand-written oracle tests or mutant feedback.

## Frozen compact benchmark

Source-size/import inspection was done before model efficacy outcomes:

| Project | Commit | Selected modules |
|---|---|---|
| genty | 85f7c960a2b67cf9e58e0d9e677e4a0bc4f05081 | genty.genty_repeat; genty.genty_args |
| woa | 474737951cb0b0952e245e666e66ea51835cfd07 | src.whale_optimization |

These are in the paper's NA frame. The proposed earlier pyrthon/superstring set
was not locked: inspection found an empty pyrthon.console and 37 functions in
superstring. The actual chosen frame is **3 modules in 2 projects**, not five modules
in three projects. Do not silently claim the original proposed size was executed.

Small stage: genty.genty_repeat + genty.genty_args, seed 42, 1 round, 2 arms
(4 module trials, 2 project workers). Same model and budgets as the larger stage.
Larger pilot: all 3 modules, seeds 42/43, 3 rounds, 2 arms (12 module trials).
The small module/project are development data. This frame is not held-out evidence
of generalization; use other locked projects for a later confirmatory study.

Model load/repeated initialization and project costs are not per-module costs.
Raw inspection with SCRIPTED summaries found 95 initialization calls/20 graph edges
in genty and 59 calls/14 edges in woa. These are not predictions of exact real-model
call counts/timing, but explain why shared initialization reuse matters.

## Hardware and progression gates

Open `notebooks/kaggle_upstream_nf4_paired.ipynb` with Internet and GPU T4 x2.
It clones a pinned public Git base and applies a transparent SHA-256-checked local
source snapshot. No separate source ZIP is required. Changes are not claimed pushed.

Run All stops after small. Steps:

1. Source regression tests with GPUs hidden.
2. `plan`: freeze code/config/target frame and budgets before model outcomes.
3. `prepare`: pinned checkouts, per-project venv/dependencies/import provenance,
   source hashes and deterministic mutant pools. No model inference.
4. Real upstream CPU initialization on both actual projects with SCRIPTED summary/
   embedding fixtures; then real upstream generation/scoring on a temporary toy
   project with SCRIPTED outputs. Their artifacts are engineering evidence ONLY.
5. `stress`: on each GPU in parallel, synthetic source token inputs up to the
   frozen cap with FORCED full-budget decoding and a repeat of the largest input.
   The current notebook freezes 4096 input + 512 output for both stages/arms.
   Require at least 1.5 GiB
   conservative headroom. Weights-only fit is insufficient. Input and output budgets
   and immutable model revision are bound to the evidence. No efficacy metrics.
6. `small`: actual Qwen 14B inference through upstream for both arms, isolated
   processes/checkouts, at most one worker per GPU. Actual prompt overflow/OOM and
   incomplete workers block the larger stage, even if model loading succeeded.
7. Review source/test evidence and measured runtime, then explicitly enable
   `RUN_LARGER` in the last cell. Main refuses missing/mismatched stress/small evidence.
   A baseline producing no valid tests is an outcome, not a reason to fabricate pass.

The GPU screen has one 3600-second wall-clock budget spanning stress model
download/load, bounded embedding download and the small workers. CPU environment
installation, preparation and scripted engineering fixtures are separate overhead.
Each probe is capped at 1800 seconds; both GPU probes run concurrently. Worker
timeouts use the remaining shared budget. A budget timeout preserves planned
rows/raw artifacts and blocks larger readiness; it is not a successful screen.
At least one real model-generated retained-test coverage path must be measured
in small before larger can start. This is a development engineering criterion,
not proof of generalization or a requirement that baseline be all-pass.

No automatic favorable-seed retries or replacement project. Worker limit is one
hour per project/arm/seed; unfinished work remains in the planned denominator.
Context overflow is recorded, not silently trimmed. To change budgets after a
hardware failure, preserve the output and make a NEW plan; use the same budgets
for both arms. No GPU/model memory measurements have been made locally.

CLI after installing `requirements-paired.txt` in the modern environment:

```bash
python paired_study.py --action plan --output /kaggle/working/PAIRED
python paired_study.py --action prepare --output /kaggle/working/PAIRED
python paired_study.py --action stress --output /kaggle/working/PAIRED --jobs 2
python paired_study.py --action small --output /kaggle/working/PAIRED --jobs 2
# Only after the small evidence is reviewed:
python paired_study.py --action run --output /kaggle/working/PAIRED --jobs 2
```

Default budgets can be changed only at planning, e.g. `--max-input-tokens 4096
--max-new-tokens 512`, then preserved for all later actions. This is a new condition,
not a hidden fallback. Settings/code drift prevents continuing the same study.
Rebuild the self-contained notebook with `python scripts/build_paired_notebook.py`.

## Metrics and interpretation

Retain all generated versions, deterministic patches, import/type facts, assertions
before/after upstream repairs, reductions, generation errors, source hashes, stage
costs, raw model calls, logical vs fresh tokens and cache-hit flags.

Primary early evidence: original-passing nodes replayed for module line/branch
coverage, outcome/measurement denominators, and paired target/seed differences.
Incomplete workers, unknown framework exceptions and resource-budget errors block
larger readiness and are not used as successful paired comparisons.
Missing/no-branch values remain NA. Import-time/module coverage is not target reach.

Secondary fault measure: up to FOUR deterministic arithmetic/comparison mutants
per module, frozen before model execution, same pool for both arms. Scores require
stable original-passing nodes and every mutant resolved. Import/setup/collection/
timeout failures are inconclusive, not kills. No operators -> NA (genty_args currently
has none); no eligible tests -> NA with explicit failure counts. Equivalent mutants
are not filtered. This small pool is not a broad mutation benchmark or semantic
assertion-accuracy estimate. Mutant verdicts never enter inference/repair.

Initialization fresh-token/time differences reflect cache order/warmth, not method
speed. Compare generation/repair costs separately and report total shared-prefix
cost. The same project cost is repeated in module CSV rows for provenance; do not
sum it per module. Two seeds and three modules support descriptive pilot results,
not significance claims or superiority to the published GPT-4o results.
