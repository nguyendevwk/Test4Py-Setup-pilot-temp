# Source-only API contract experiment

The proposed contribution is a bounded static API contract for small-model test
generation, implemented in `pilot/api_contract.py`. It distinguishes a property
from a method, records real signatures and locates the enclosing callable of a
nested function. It does not execute production code or supply expected outputs.
The hypothesis is fewer invalid API calls and more tests that reach the real
target, at a measured additional input-token cost. An implementation alone is
not evidence of an effective or novel research contribution.

## Locked development comparison

`research/benchmark/api_contract_development_probe.json` fixes five genty targets
and ten planned arm trials. These targets were used to diagnose previous failures
and are development data. Initial prompts come from actual upstream generation
calls, with no repair feedback. Both arms receive the same concise complete-file
instruction; multiple test functions are allowed. Only `api_contract` receives
the bounded source facts. The legacy bundle called `improved` is absent.

The fixed 14B revision, NF4 settings, seed 42, temperature 0.7, top_p 0.95,
4096-input and 512-output caps are shared. Arm assignment alternates across GPUs
by target. Each GPU must first pass same-session repeated full-capacity stress
checks. Model-load and inference costs are retained. A source archive freezes the
running implementation; local changes do not modify an in-flight cohort.

`scripts/api_contract_probe.py` performs one initial generation per trial, with
no repair, test filtering or selective reruns. It retains raw responses, prompts,
token counts, extraction/collection errors, all tests and production source
hashes. A nonempty all-pass suite must replay with the same passing node set.
The diagnostic primary outcome is an all-pass stable suite with positive target
function coverage; raw first-pass rate and module line/branch counts are separate.
No branches means NA. Missing coverage remains NA. A capped output is retained
as an unsuccessful generation, not repaired off the record.

Assertions still require semantic review. Syntactic quality checks cannot prove
oracle correctness or prevent every reimplementation. A tiny pre-existing mutant
pool is supplementary evidence only; a target with no eligible mutant has NA
fault-detection evidence. Any apparent gain must survive review for hollow tests,
wrong assertions, target substitution and weakened checks.

This fixed-input diagnostic measures the generation component, not a complete
upstream Test4Py run. Its result cannot establish superiority over the paper.
In the separate end-to-end adapter, both arms use the same assertion-preservation
acceptance policy; the legacy asymmetric acceptance policy is not the new control.

## Held-out frame and decision rule

`research/benchmark/api_contract_heldout_frame.json` was locked before model
outcomes: 12 distinct modules, four projects and three seeds per target, giving
36 paired comparisons / 72 planned arm trials. Its SHA-256 is
`c2ceaae4e0c8374a2e18ebc6ddbbd900f7e5f6bb0d237d12bd4aba10b1c3a9c3`.
Selection uses only pinned source eligibility and deterministic stratification,
not model success. Development projects are excluded. Two property targets, two
closure targets and eight ordinary callable controls are included; this is not
a balanced or representative sample of the paper benchmark.

This is a locked selection frame, not evidence that all environments or model
trials have run. Dependency/import preparation must finish before inference.
Failures stay in the planned denominator and are never replaced with targets
that produce better results. Preparation must record installed dependencies,
source hashes and module origins, without changing production code. Seeds are
within-target repetitions; four project clusters impose substantial uncertainty.
No fixed sample count guarantees significance.

Before held-out inference, freeze prompt construction, scoring, caps, execution
environments and the mechanism revision. If a mechanism is changed after seeing
held-out outcomes, those outcomes become development evidence for that revision.
Report paired target and project effects and uncertainty, plus API-error labels,
reviewed assertions, fault detection, output truncation and cost. Coverage gains
from dropping failing tests or weakening assertions do not count as improvement.

A useful outcome can be higher reviewed quality at matched cost, or comparable
quality on a smaller model with a measured resource saving. Comparable quality
requires a predeclared acceptable margin and uncertainty; an inconclusive
difference is not evidence of equivalence. No 7B result has been established by
the 14B diagnostic. A complete matched upstream evaluation and independent fault
evidence remain necessary before making a paper-level improvement claim.

The historical `single-test-v1` constraint failed during model execution and is
not part of this mechanism. It must not be quietly reintroduced as a way to
discard valid multi-test files.

## Observed v1 outcome and next development ablation

The completed v1 diagnostic has 0/5 baseline and 1/5 API-contract stable,
target-reaching suites. All ten attempts remain. Treatment input tokens increased
21.67% (5869 to 7141 total), and summed inference time increased 5.94% (240.87 to
255.18 seconds). There is one project cluster. This is an exploratory signal,
not a general improvement or equivalence result.

The successful six-test suite covers repeat metadata and rejects invalid calls;
it does not prove that an entire test runner repeats execution correctly. A
report/product directory collision interrupted mutation scoring. A separate CPU
recovery replayed the identical candidate on the same runtime and killed the
original fixed boundary mutant, without generating or editing a test. The
original error is retained. See
`research/artifacts/api_contract_v1_development_audit_20261117.json`.

Property-call and nested-import mistakes persist in both arms. The original
upstream inputs contain generated usage examples that contradict decorators and
lexical ownership; appending correct facts did not reliably overcome them.
The next development cohort is explicitly a different protocol:
`research/benchmark/api_source_development_probe_v2.json`, with five targets,
three arms and 15 planned model calls. It re-generates its baseline and does not
pool outcomes with v1. `source_only` replaces generated descriptions with
AST-rendered pinned production source. `api_contract` uses that same source plus
the facts, separating source replacement from the additional inventory. Only the
development outcomes informed this change; no held-out model outcomes were used.
Changing the whole source context is a separate mechanism, not a claim that v1
facts alone caused any v2 gain.

All twelve held-out target imports subsequently passed CPU preparation on four
isolated project environments. dfsql needs Python 3.9 for its unmodified
`collections.Iterable` import; the other projects use Python 3.11. Coverage 7.6.1
and pytest 8.3.5 are common across these test environments. These differ from the
development model/test environment and will define a separate held-out cohort.
`pymssa` also requires its source-imported, undeclared scikit-learn dependency.
Exact resolved packages and source hashes are recorded in
`research/artifacts/api_contract_heldout_preflight_20261117.json`. Import success
does not validate target state synthesis, assertions, generation or efficacy.

The v2 development cohort has completed: upstream prompt 0/5, source-only 2/5,
source plus facts 3/5 stable target-reaching suites. Compared with source-only,
facts win on both getters, lose on the closure and tie on the factory and outer
decorator. Summed generation time is 236.05 / 208.12 / 167.46 seconds for the
three arms; this excludes model load and shared preparation. The candidate getter
assertions were reviewed against source, including positional/keyword separation
and actual iterator string formatting. Those getters still have no eligible
mutants in the original tiny pool. See
`research/artifacts/api_source_v2_development_audit_20261117.json`.

## Locked independent-project component comparison

`research/benchmark/api_source_heldout_component_v2.json` retains all twelve targets
from the original source selection frame, expands seeds 42/43/44, and locks 72
trials. Its SHA-256 is
`e89de4086cf3ba2ab2d62fafe59709a792a5e129dd297c801002f404e78bf6e5`.
This is an additional component protocol: its control is `source_only`, not the
original upstream summary/RAG prompt. Both arms have identical trusted source;
the treatment adds only API facts. The original frame and development cohorts
remain unchanged. Model budgets are 4096/512, one generation, zero repairs and
no pruning. Runtime compatibility and exact dependency locks are checked on
Kaggle before inference. Source-selection hashes and the model revision must match.

The explicit entrypoint is `scripts/run_api_heldout_component.py`. It does not
launch a full paper campaign. The 14B run
`API_HELDOUT_COMPONENT_20261117T025213627216Z` passed all twelve imports on Kaggle
and started the fixed inference schedule. No mechanism/prompt/scoring adjustment
is permitted in response to its outcomes. `pilot/api_probe_analysis.py` preserves
unknown attempts, pairs by target/seed, and reports project effects; its bounds
for missing outcomes are not statistical confidence intervals. Four clusters
and three repetitions per target do not warrant strong significance claims.

During preparation, a mutation-pool bug for nested arithmetic expressions sharing
start coordinates was fixed before held-out inference. AST traversal identity now
selects the exact operator. A regression checks distinct faults in `a*b*c`; the
original simple genty pool is unchanged. A resolved-lock preparation replay then
passed all twelve imports. Earlier preparation failures and final locks/pools are
retained in `research/artifacts/api_heldout_preparation_evidence_20261117.zip`.
The local regression suite passed 180 tests, including actual pytest/replay/mutant
execution through the prepared-interpreter path. These are engineering checks.
