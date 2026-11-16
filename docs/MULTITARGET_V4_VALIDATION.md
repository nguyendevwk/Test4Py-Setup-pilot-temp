# Local validation of protocol v4 (2026-11-16)

This document records engineering evidence, not model efficacy measurements.
No v4 GPU inference has been run locally. The failed v3 Kaggle archive remains
unchanged and must not be pooled with v4 results.

- Python 3.12.13, pytest 8.4.2, pytest-json-report 1.5.0, coverage 7.10.7.
- Final full suite: **102 tests passed**, including **37 multi-target tests**.
- Tests use explicit temporary toy projects and scripted model outputs; these are
  regression fixtures, not experimental results or oracle-quality measurements.
- Generic cases include src-layout relative imports, return-type/property retrieval,
  qualified methods, constructor-scope witnesses, missing arguments, no observed
  return-value export, fixed input budgets, external pinned benchmark specifications,
  unchanged test/assertion repair gates, self-repair evidence preservation, mixed
  suites, passing-subset replay instability and distinct execution/quality gates.
- Earlier Git clone + embedded v4 snapshot integration check: 36 then-current tests
  passed in the fresh clone. The final snapshot additionally includes the execution
  vs quality-gate regression; its bytes and hashes were checked by the builder.
- Final notebook JSON and all code cells compile. The notebook embeds the exact
  current source files and reference notebook with SHA-256 verification, over pinned
  Git base e86fab21d11494277d5029ff9d1c673e5c9927b0.
- Actual pinned docstring_parser and codetiming checkout preflight passed locally.
  parse witness: function entry + normal completion with a setup value.
  Timer witness: constructor entry only; no assertion about method preconditions.

## Still unverified

Real v4 model accuracy, input-budget fit, GPU peak memory and runtime on Kaggle
Python 3.13 require the supplied eight-attempt notebook screen. The previously
observed model revisions are pinned, but context, task granularity, repair gate and
measurement conditions changed. No improvement over v3 or Test4Py can be claimed
from these local checks. Held-out projects, upstream matched controls and reviewed
fault-detection metrics are required for a research conclusion.

See [protocol and execution instructions](MULTITARGET_V4.md).
