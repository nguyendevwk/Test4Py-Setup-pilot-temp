# Local engineering validation: upstream NF4 paired pilot

Date: 2026-11-16. These are CPU/source checks, NOT real Qwen 14B or VRAM results.

- Final full suite on Python 3.12.13: **124 tests passed**, including **22 paired
  runtime/guard/planning tests**. These use CPU fixtures, not real Qwen outputs.
- Fresh Git base plus the final shipped overlay passed all 22 paired unit tests and both real
  upstream fixture arms. Model/embedding were explicit scripted doubles; syntax
  checking in this fixture used compile instead of pylint. Actual PyCG, upstream
  initialization/type/RAG/generation/repair orchestration, pytest, coverage and
  mutation scoring were exercised. The fixture confirms a non-selected helper
  remains in analysis, rather than silently reducing source context to one module.
- Actual paper project commits were downloaded and inspected before model outcomes.
  genty_repeat has 2 AST functions, genty_args 5, whale_optimization 14. Source import
  passed in the local Python 3.12 environment (six 1.17.0, numpy 2.2.6).
- Actual full-package upstream initialization with SCRIPTED summaries/embedding
  completed on genty (95 calls, 20 graph edges) and woa (59 calls, 14 edges).
  These call counts are observations of this engineering fixture, not a runtime
  promise or a measured inference/summary-quality result.
- NF4 fail-closed loading, revision/device/dtype guards, no FP16 retry, token checks
  before GPU transfer, greedy-prefix cache scope/cost accounting, stdlib patch
  assertion preservation, imported namespace contradictions/dynamic unknowns,
  class/member facts, tiny fixed mutation pools and inconclusive verdict handling
  have CPU regression coverage.
- Source/no-op compatibility adapters are explicit and common to both arms. The
  missing pytest `tests` key remains a collection failure, not a successful suite.
  Unknown framework exceptions and resource-budget errors block larger readiness.

## GPU status

Local `nvidia-smi` could not communicate with a driver; no usable NVIDIA GPU is
available to run this model here. NF4 14B fit, 6K+1K forced decode, 1.5 GiB margin,
real BGE/Chroma retrieval and actual Qwen-generated test efficacy are NOT validated
by local doubles. The Kaggle notebook runs those remaining checks in order and
stops after the small A/B stage. It never counts fixture coverage as model quality.

## Reproduction and limitations

Use [the protocol](UPSTREAM_NF4_PILOT.md) and the self-contained Git-clone notebook.
Only a 3-module/2-project pilot is configured, not all 183 paper modules. Both
models are the same 14B NF4 checkpoint, selected by immutable SHA before inference.
Project environments and full source hashes are saved. Initialization reuse is a
shared greedy prefix, not evidence of independent summary replications across seeds.
No generated-test or mutant-outcome cache is allowed. No superiority claim can be
made before actual paired measurements and oracle review.
