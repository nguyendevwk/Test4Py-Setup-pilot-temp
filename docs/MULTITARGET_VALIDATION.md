> Current v4 validation: [MULTITARGET_V4_VALIDATION.md](MULTITARGET_V4_VALIDATION.md). The following is the historical v3 check.

# Engineering validation: Council development screen v3

Validation performed locally on 2026-11-16. No GPU/model inference results were
produced. This document is not evidence of research efficacy.

## Verified

- Python 3.12.13: 89 unittest cases passed, including 24 new multi-target cases.
- Additional local Python 3.15.2 check: 89 unittest cases passed. Python 3.15 is
  outside the modern Kaggle profile; the supported-version check above is primary.
- New checks execute real pytest/coverage subprocesses against temporary toy code;
  scripted model answers are fixtures, explicitly not LLM measurements.
- Extraction diagnostic blocks, ambiguous/incomplete modules, illegal `global`,
  collection counts, line/branch formulas, branchless modules, missing metrics,
  mixed suites, test deletion, changed assertions, malformed repair, timeout,
  replay instability, source modification, API checkout provenance, setup failure,
  engine failure preserving all six rows, offline mock exclusion and notebook cell
  syntax were exercised.
- Actual target checkout preflight passed on Python 3.12: docstring_parser
  `a8e2a3ba5a4cdd906830735cb41a6a22c9346bf4`, codetiming
  `e51e4c3a50a395e301c33013cd048182f961f369`.
- The actual target preflight imported APIs from their own checkout and executed
  curated setup snippets. It did not execute generated model tests or assess oracle
  correctness. These commits are now pinned for the small Kaggle plan.

## Still required on Kaggle

Run the supplied notebook with updated source. It first runs all 24 new checks
using the Kaggle interpreter/venv, preflights the pinned checkouts, then executes
six model attempts. NF4/model loading, GPU memory, real output format, test quality
and repeatability on Kaggle Python 3.13 have not been verified locally.
A successful local check cannot guarantee the full experiment will pass.

The automated readiness gate is conservative. Keep every failure and review
assertions/target reach even if it passes. No pruning, seed cherry-picking,
assertion weakening, mutant feedback or favorable-score selection is permitted.
For research claims, use a separate locked protocol with upstream controls and
held-out targets. This screen cannot demonstrate improvement over Test4Py's paper.

See [the execution guide](MULTITARGET_SMOKE.md) for the fixed plan and artifacts.
