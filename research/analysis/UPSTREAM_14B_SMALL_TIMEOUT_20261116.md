# Upstream 14B small — cold initialization timeout

Archive `UPSTREAM_NF4_RESUME_20261116T174754946339Z.zip`, SHA256
`603266e8f6360ae0fc86d93d2bed7edc131db23a81448017a80202518d566b3a`.
Read on 2026-11-17. Raw extraction is in
[the audit](../artifacts/upstream_14b_small_timeout_audit.json).

## Result

Both workers were killed by the prescribed deadline: returncode -9,
`timeout=true`, ~3587.3 seconds per worker, after ~13 seconds of preceding work.
None of the four planned module trials completed final scoring. Line/branch
coverage, mutation and paired differences are NA. This is an engineering-budget
failure, not measured zero test accuracy or proof one arm is better.

Original `report.json` still says `running` because a SIGKILL cannot write a
final report. Parent reporting now derives terminal timeout from process.json.
Original `finished_module_rows=4` counted placeholder rows, not completed
measurements. Future reports distinguish reported rows from completed trials.
Original observed-success/planned bookkeeping0.0 must not be presented as
assertion accuracy; future all-unmeasured pass rates are null with an explicit
rate-status field. The original archive remains unchanged.

## What actually ran

| Item | Baseline | Improved |
|---|---:|---:|
| Completed model calls | 122 | 121 |
| Initialization calls | 95 | 95 |
| Generation/repair/type calls | 27 | 26 |
| Recorded model-call exceptions | 0 | 0 |
| Initialization calls at512-token cap | 5 | 5 |
| Generation-phase calls at cap | 4 | 3 |
| Candidate extraction exceptions | 3 | 2 |
| First generation event, elapsed seconds | 2627.48 | 2627.13 |

Model loading took ~147.5 seconds. Full initialization plus loading/indexing
consumed ~43m47s before generation, leaving only ~16 minutes for seven selected
functions, repair and scoring. The original one-hour estimate was optimistic.
Repeated heartbeat lines did not prove a hang: raw events show continuing model
calls that the compact console filtered out.

Baseline has two intermediate files accepted by upstream, but no complete module
evaluation/replay/mutation. Do not turn those partial observations into final
success credit. An improved repair was accepted by upstream after modifying/
removing checks; the preservation audit vetoed it. This demonstrates that the
guard can refuse such a proposal, not that semantic assertion correctness is
proved for every accepted test.

Actual API/oracle mistakes include calling `GentyArgs.kwargs` as a method and
expecting incorrect `__iter__` formatting. Obsolete `.pylintrc` option warnings
also appear; they are not a sufficient explanation of all failures. Output-cap
hits and extraction failures must be distinguished; not every cap hit proves an
incomplete test and not every extraction failure has the same cause.

## Observational fixes and bounded continuation

Progress now tracks stage items, function/round counts, module/mutant counts,
workers completed, elapsed/remaining budget and dynamic model-call counters.
The previously untracked function-database indexing is a separate 11th tracked
initialization step. Progress100% means work processed, not tests all-pass.
Structural progress is no longer hidden by the compact model-event display cap.

The 95 unique greedy initialization prompts/cache outputs were verified against
the original raw model logs, model/runtime revisions, source inventory and exact
cache keys. A warm-prefix screen can re-key these same prompt/output pairs after
observational code changes. It imports no generation, repair, test or scoring
outcomes, preserves all five capped summaries and reports original cold cost
separately. Changed incoming prompts miss the cache normally. Both arms receive
the same initialization reuse. This does not make cold execution a one-hour run.

Do not start the larger configured pilot until a real small worker/measurement
path completes and its test/oracle evidence is reviewed. No superiority claim
against the original paper follows from this timeout or the memory stress.
