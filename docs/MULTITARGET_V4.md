# Council development protocol v4: SLM source grounding

This is a NEW development cohort, not a replay of v3, not Test4Py upstream, and
not evidence of improvement over the paper. The two previous targets have already
informed development; exclude them from held-out generalization claims. Preserve
the failed v3 archive unchanged. No full experiment is launched automatically.

## Hypotheses and fixed ablation

The mechanism reduces the reasoning burden of an SLM using production source,
without supplying observed return values, hand-written expected assertions or
mutant outcomes. All arms share model revisions, token caps, focused-test prompt,
repair policy, executor, seeds and metrics. Only context/verification varies:

| Arm | Context |
|---|---|
| baseline | Target source + runtime API inventory; Council without setup |
| grounded | baseline + bounded source dependencies, including return-type definitions |
| ranked | grounded + curated setup hint; no ranking algorithm is claimed |
| verified | ranked + witnessed target entry/normal completion, or constructor entry for a class |

Comparisons: grounded-baseline estimates context augmentation; ranked-grounded
estimates the added curated hint; verified-ranked evaluates invocation evidence
and failure gating. This is not proof of automatic setup synthesis. A constructor
witness does not establish every method's preconditions. Unresolved setups stay
in the planned denominator; do not exclude difficult targets after seeing scores.

## Generic implementation and SLM budgets

- Source retrieval follows definitions/imports and return annotations in production
  Python AST, to depth two, at most ten snippets and 10,000 source characters. It
  never scans tests or outcomes. Whole definitions are included or recorded as
  omitted, never silently cut mid-definition. Dynamic/star/module alias import
  patterns and complex runtime types remain limitations. Context is not guaranteed
  complete on arbitrary projects.
- Qualified `Class.method` targets retain source from the containing class so
  constructor/state transitions can be inspected. Relative imports and `src/`
  layouts are supported. There are no project-name branches or per-case expected
  values in the algorithm.
- Each generation requests one focused behavior and one test function, at most
  60 lines. Actual count is recorded; tests are never deleted to enforce it.
  Parameterized nodes still count as separate executed tests.
- Input cap: 8192 tokens measured by the selected role's tokenizer. Overflow is an
  explicit failed attempt, not silent context truncation. Output cap: 2048 tokens;
  truncated or ambiguous code is not salvaged. These budgets are experimental;
  GPU fit and quality still require a real run.
- One repair call, no retry on timeout, same policy across arms. Diagnostics are
  compact per-node failures. `--repair-with coder` allows a separate self-repair
  cohort without loading Critic; default remains Critic for this screen.
- Automatic repair acceptance requires preserved test names/counts and unchanged
  assertion expressions under the existing syntactic audit. Changed proposals are
  saved but receive no automatic final-pass credit. This gate cannot prove oracle
  correctness or detect all semantic weakening; independent review remains required.

## Metrics and integrity

First-pass and final full-suite pass retain every failed node. No pruning.
Main module coverage is measured only for all-pass suites. A secondary
`passing_subset` metric re-executes the original-passing nodeids twice from the
UNCHANGED suite. It reports eligible/planned, stability and module coverage, and
never changes suite pass. If subset execution or coverage is unstable/missing,
secondary coverage is NA. Replay processes are fresh; external filesystem/global
resources may still affect reproducibility. Hash all product Python source before
and after evaluation; modification invalidates both coverage metrics.

`replay_status=not_run` is distinct from `unstable`.
`harness_ready` identifies a complete queue with execution evidence and no reported
infrastructure/source-modification error. `automated_ready` / `generation_quality_ready`
retain the strict all-planned-suites quality gate. A failed baseline remains a failed
baseline even if the harness ran correctly. Return code 2 still indicates the strict
gate failed; this separation does not improve any test score. Module coverage is not target
coverage and may include import-time lines. Readiness is only an engineering gate;
assertion correctness, meaningful target reach, mutation and real-fault efficacy
still need separate evaluation. v4 does not implement a general mutation benchmark.

Record `plan.json` before inference, all prompts/raw answers, token costs, immutable
revisions, source hashes, omitted dependencies, invocation code/process logs,
repair proposals/audit and every failure. Model call ids include target/arm/sample.
No seed selection, score-driven target exclusion, expected-value copying, hidden
repair budget or silent model fallback is allowed.

## Run the small Kaggle screen

Upload `notebooks/kaggle_git_clone_smoke_v4.ipynb`; enable Internet and T4 x2.
It clones a pinned Git base plus a transparent, SHA-256-checked local source
snapshot. No source ZIP is needed. It runs source regression tests, prepares the
pinned target checkouts, and runs **2 targets x 4 arms x 1 attempt = 8 outcomes**.
Model SHAs are the same as the observed v3 run. Conditions otherwise changed;
do not infer a method effect by pooling/contrasting v3 and v4 as a matched study.

The notebook retains failures and creates a review ZIP. A red gate must not be
made green by deleting tests, choosing favorable seeds or changing expected values.
A green gate still requires assertion/target-reach review before a full study.

Rebuild the embedded snapshot after code changes:

```bash
python scripts/build_smoke_notebook.py
```

## Other benchmark projects

Supply `--target-spec PATH` with a JSON list or `{"targets": [...]}`. Every target
needs `id`, `project`, `repo_url`, immutable 40-character `commit`, `module`, relative
production `file`, and `symbol` (function/class or qualified method). An optional
`setup_hint` is explicitly curated code, not mined evidence. Without a valid
witness the verified arm reports setup_unresolved; other arms may still run.
Install dependencies before preflight; the runner never installs them during runs.

```bash
python council_multitarget.py --target-spec locked-targets.json --prepare-only --output /kaggle/working/PREP
python council_multitarget.py --target-spec locked-targets.json --prepared /kaggle/working/PREP/preflight.json --output /kaggle/working/RUN
```

Use fresh paths, actual output paths and a locked plan. Project-level dependency
incompatibilities need isolated environments, not silently replacing repositories.
Evaluate multiple held-out projects and pair results at target/project level.
Multiple seeds on one target are not independent targets. Add matched upstream
Test4Py controls before making claims about replacing its original model.
