# Nineteen-module NA-subset baseline

This extends scope beyond the original single-function pilot. It does NOT claim
that the PyCG-specific setup synthesis generalizes to other subjects. Stage1
establishes a runnable upstream Test4Py baseline with the same small model.

Population: the pinned Test4Py `projects.json` lists183 modules in26 projects.
The NA subset has58 modules in9 projects; this batch selects19 from that NA
frame, project-balanced, seed42, fixed before seeing outcomes. Thus it is19/183
in size (10.38%), **not a random representative10% of all183**, and32.76% ofNA.
No source/dependency failure is replaced with an easier module. A full183-frame
sample also requires verified provenance for the Pyn subjects, which is not
supplied by `projects.json` alone. This batch deliberately uses Table1 NA
repository/commit entries whose provenance is published.

Sources:
- https://arxiv.org/html/2503.14000v2#S4.T1 (Table1, NA repo/commit prefixes)
- https://github.com/Test4DT/Test4Py/blob/3c8b45410545183a9a579a784ffefae722a158a6/projects.json

`na-projects.json` preserves the paper's commit prefixes. GitHub's commits API
resolves a prefix to40 hex digits before checkout; both prefix and full SHA are
saved, and the checked-out HEAD must match. No branch HEAD is substituted.
`projects-upstream.json` is checked against the freshly checked-out upstream
before execution. Selection does not read existing tests or outcome artifacts.
Model/embedding revisions are resolved and recorded once before model loading.

Actions:
- `--action plan`: offline, no model/dependency/source download.
- `--action prepare`: per-project isolated venv, source commit, package install
  constrained by our runtime pins, and imports; **no model inference**.
- `--action run --resume`: continue the identical plan/source/config after prepare;
  skip execution-complete projects, preserve previous failed attempts separately.
  Existing prepare failures are retried and never counted as quality successes.

Three rounds by default; every selected module's functions use upstream
TestManager generation/repair and upstream coverage feedback. Initial analysis
uses all production sources of the package, excluding test paths. A production
source excerpt and deterministic code-block extraction are common baseline
adaptations for the local SLM, documented as new conditions, not exact GPT4o
paper reproduction. Selected modules share project initialization and costs;
there is no cross-project interpreter/import cache. One worker per visible GPU.

Module quality is scored from original-passing tests assigned to that module's
generated files, then replayed for branch coverage. Ownership is explicit in
`test_ownership.json`; incidental coverage from another module's tests is not
credited. For src-layout projects, package import root becomes pipeline root;
this deviation is recorded in worker settings. Every missing/incomplete outcome
is reported; mean coverage is explicitly conditioned on scored modules and must
be read together with scored/19 and original-pass counts. No branch denominator
means NA, not100%. No general mutation operators or semantic oracle audit have
been implemented here: those fields stayNA. PyCG's two custom mutants are not
applied to unrelated modules.

`reference_*` columns optionally read matching module coverage from the pinned
upstream's ex1 artifacts. Reference is descriptive: different models, runtime
and conditions prevent attributing differences to the setup extension. There
are no fabricated confidence intervals, inferred type-accuracy scores, or
claim that passing tests alone prove semantic correctness.

Save `plan.json`, `benchmark.json`, `modules.csv`, `report.md`, and project logs,
source_revision.json, requirements-resolved.txt, worker-settings.json, raw model
calls, attempts, checks, retained Test4DT_tests, original pytest and coverage.
Keep the output as a saved Kaggle Notebook version; a session directory alone
is not durable. Partial runs can be resumed only with identical runner hashes
and settings. Network or GPU tests have not been executed locally; offline
selection/statistics tests and CLI plans are the local validation evidence.
