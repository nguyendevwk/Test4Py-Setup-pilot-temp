# Quality-first evaluation and model selection

Status: proposed next cohort, not executed. Existing out_v2 is preserved and has no retained passing tests. Do not claim cost effectiveness from lower tokens when usefulness is absent.

## What accuracy means

Separate AST parsing, static-gate acceptance, original execution, receiver-state validity, target reach, oracle correctness, and fault detection. Original passing is necessary, not sufficient: tautological assertions and tests that never instantiate the returned loader can pass without validating required behavior. An executable percentage is not type accuracy, semantic accuracy, or coverage.

Existing audited cohort: initial AST valid4/4; initial and final upstream static-gate valid0/4; repaired AST valid3/4. Four treatment candidates are not four independent targets. Runtime first-pass accuracy, semantic oracle accuracy, type-prediction accuracy, loader reach, branch coverage and mutation score cannot be reconstructed from these static-gate failures. Preserve missing values. Numeric AST assertion counts can include fixtures/irrelevant checks, so never call them meaningful assertion counts without review.

## Published reference versus reproduction

Paper v2 reports 183 modules, mean statement83.0% and branch70.8%. Its type study reports relaxed user-defined accuracy63.5%; mutation comparison reports Test4Py0.843 against NoGraph0.787 using mutmut on runnable projects. These are separate experiments, populations and denominators. Source: https://arxiv.org/html/2503.14000v2

Our one-function, one-round SLM pilot does not reproduce those aggregates. Report published references in a separate table; never subtract our NA from their percentages or call 83% test accuracy. To attribute the extension, compare baseline/caller/extracted/verified with identical backend and scoring within each model; model selection is a separate factor. A model upgrade is not setup contribution.

## Primary quality measures before costs

1. Initial candidate executability: candidates passing original before repair / all initial candidates. Include failed generation/import candidates in end-to-end denominator. Explicitly distinguish candidate/file and pytest-node units.
2. Final useful-scenario success: scenarios with an original-passing test that reaches loader __init__ and checks specified observable behavior / two declared scenarios. Require absent creation and old-path preservation; audit assertions internally, never put oracle values in prompts.
3. State validity and reach: count fresh receiver setups satisfying prerequisites and tests actually invoking returned loader construction. Trace per node; exceptions alone do not classify state failures.
4. Target+nested statement/branch coverage with explicit concrete line/arc denominator; report full module coverage separately.
5. Assertion adequacy: matched before/after repair assertions, removed checks, nonvacuity, independently audited expected behavior. Do not infer semantics from assertion counts.
6. Fault detection: same two illustrative mutants, only original-passing nodes, killed/survived/environment/timeout separately. Internal handwritten oracle stays excluded.
7. Stability: at least three fresh-process replays of retained nodes; record per-node disagreements. This detects some flakiness, not proof of universal stability.

Pilot engineering acceptance proposed: chosen backend/configuration must produce original-passing, target-reaching meaningful checks for both scenarios and kill both illustrative mutants without injecting an oracle, on repeated clean replay. This is a pilot smoke gate, not a threshold demonstrating superiority. Report every failed model/configuration. Only after passing assess actual tokens, end-to-end seconds, peak memory and cost per useful scenario.

## Small-model shortlist checked 2026-11-14

- Qwen/Qwen3.5-4B: primary 2026 candidate. Vendor card reports LiveCodeBench v6 55.8; coding benchmark is not pytest accuracy. qwen3_5 and multimodal wrapper/runtime need dedicated support and pinned compatible Transformers; current4.57.6/AutoModelForCausalLM path is not declared validated. Text-only execution and fp16/KV measurements required. Source https://huggingface.co/Qwen/Qwen3.5-4B
- Nanbeige/Nanbeige4.1-3B: independent 2026 3B candidate. Validate tokenizer/chat/reasoning/final answer and EOS handling; card's very large generation recommendation cannot be replaced silently with512. Save raw reasoning and final output separately and account for both. Source https://huggingface.co/Nanbeige/Nanbeige4.1-3B
- Qwen/Qwen3-4B-Instruct-2507: compatibility/control candidate available in2026, released2025. Non-thinking and causal-LM interface reduce extraction ambiguity. Source https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507
- Historical control: Qwen/Qwen2.5-Coder-1.5B-Instruct pinned existing revision. Keep failed observations; do not relabel as competitive because cheap.

No universal best-model claim: vendor task scores have different protocols and do not directly rank test generation. Pick model by measured pipeline quality, not popularity. FP16 weight-only estimates3B~5.6GiB,4B~7.5GiB exclude vision, embedding, KV cache, activations and allocator. Actual 15GiB fit requires smoke measurement; two15GiB GPUs do not automatically form one30GiB device. Keep one worker per GPU initially; embedding on CPU can be an engineering cohort change applied uniformly.

## Fair selection and execution

Use the same pilot target only, respecting scope. Candidate screening is development, not held-out generalization evidence; disclose target tuning. Resolve immutable revisions and pin full environment. Validate one model's class loading, dtype, tokenizer/EOS, chat system role and complete final-code output before costly initialization. Record loader/runtime failure independently from model-code failure.

Use documented non-thinking mode when supported; reasoning models need explicit reason/final parser and sufficient total reasoning+answer budget. Common initial trial output budget2048 is a proposal for non-thinking generation/repair, not a proven optimum; reasoning-model budget must be validated. Parse a single complete fenced Python block with a common deterministic rule and retain raw text. Do not silently rewrite imports/assertions. New budgets/templates/runtime form a new cohort. Within a selected model, keep all four arms' generation policy identical. Common fixes for hallucinated summaries must affect every arm; upstream provenance and resulting prompts remain reviewable.

For fair quality ranking, predeclare quality metrics and allowance (repair attempts, maximum context/output, timeout); explicitly disclose model-specific templates, tokenizer tokenization and reasoning budgets. Equal token limits across tokenizers are not equal compute. Rank useful-scenario success and meaningful fault detection first, coverage second; use cost for configurations meeting quality gate. Do not optimize cached summaries until equivalence is demonstrated; separately charge cold/warm costs.

No new GPU/model run was executed in this evaluation. Local artifacts under research_reports/quality-first are deterministic audits of supplied out_v2, not results from any shortlisted model.

## Implemented integration pre-screen

`smoke_pilot.py` provides an explicitly separate small stochastic sample queue:
1attempt first, then10% of100 (10 attempts), optionally100 after review.
It preserves raw logs, fresh source directories/processes, common scoring,
passive constructor traces and replay outcomes. It does not execute upstream
initialization/repair and cannot be reported as Test4Py efficacy. Profile metadata
records original publisher, model kind (base/instruct/reasoning), license and
paper. Default Nanbeige is a post-trained reasoning model, not a base model.
Base models need a distinct validated completion prompt adapter; silently applying
the chat adapter to arbitrary base checkpoints is not supported evidence.

### Latency-driven candidate update

Following observed Nanbeige905-token output for a trivial add function, prefer
Qwen3-4B-Instruct-2507 for the next bounded screen: non-thinking by model design,
2048 output cap, official checkpoint and Apache2.0. This is a2025 checkpoint
selected for2026 research, not claimed to be released2026 or globally best.
Keep Nanbeige as an explicitly selected2026 reasoning comparator. Add the
Qwen2.5-Coder-3B-Instruct code specialist (qwen-research license) as an alternative.
Compare original-pass/target reach/mutation/replay first, then measured latency;
no expected speedup is reported as observed. Do not transfer the old long-run
quality results to these untested configurations.
