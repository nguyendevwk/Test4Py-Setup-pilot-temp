# Small 14B NF4: remote Kaggle execution, 2026-11-17

## Prior cold-prefix screen

Archive: `UPSTREAM_NF4_RESUME_20261116T174754946339Z.zip`.
SHA-256: `603266e8f6360ae0fc86d93d2bed7edc131db23a81448017a80202518d566b3a`.
The local raw copy is under `kaggle-output/remote-20261117/` (Git ignored).
Machine-readable audit: `research/artifacts/nf4_14b_small_timeout_20261117.json`.

Both real workers timed out after approximately 3587 seconds. All four planned
module trials remain incomplete; coverage, mutation and semantic accuracy are
unavailable. This is not a measured 0% generation-quality result.

Each arm logged 95 initialization calls (approximately 2354 seconds including
shared-cache waiting). Across both arms these comprise 95 fresh calls and 95
cache hits. Generation then completed 27 calls for baseline and 26 for improved
before timeout. These counts exclude unfinished calls and do not equal completed
test suites or independent samples.

## Source-based oracle notes for review

These notes refer to the locked production source, not observed mutant results.

- `GentyArgs.args` and `.kwargs` are properties returning a tuple and a dictionary.
  Calling `.args()` or `.kwargs()` is an API error.
- Iteration formats positional arguments as strings and sorts keyword names.
  String values use `repr`, including quotes. For example,
  `list(GentyArgs(1, 2, name='Alice', age=30))` should yield
  `['1', '2', 'age=30', "name='Alice'"]`.
- `genty_args(*args, **kwargs)` returns a `GentyArgs` instance.
- `genty_repeat(count)` rejects negative counts. Its returned decorator stores
  `genty_repeat_count` and returns the same function. Applying that decorator
  alone does not execute the function. Expansion belongs to the surrounding
  `genty` class-decorator machinery.

The prior generated `genty_args` files contain property-call errors and incorrect
iteration expectations. Accurate constructor checks in the same files do not
make those incorrect assertions valid. A passing suite still requires review.

## Warm-prefix engineering retry

Run: `UPSTREAM_NF4_RETRY_20261116T190701623856Z`.
The user authorized execution through the existing Kaggle Jupyter server.
The connection URL is excluded from repository files and reports.

A fresh source clone and source-hashed overlay retain the same model, immutable
model revisions, production sources, settings, modules, seed and one-round
budget. Preparation, environment freezes and the earlier real two-T4 memory
calibration passed reuse checks. Four reuse tests and three progress tests passed
locally before launch.

The retry imports 95 exact greedy initialization prompt outputs, validated against
prior model-call logs, cache keys, source, runtime and model revisions. Five of
these prior outputs reached the output-token limit; reuse does not establish
their semantic accuracy. No generated tests, repairs or scoring outcomes are
imported. Previously spent cold initialization cost remains in the prior run;
warm costs cannot be presented as an unconditional treatment speedup.

Completed: all four planned rows were reported in 2053.06 seconds of launcher
wall time. The original ZIP SHA-256 is
`604d75c7e03bca094984d51bf4421860b6772c589df69f6866b1fbed11a0dcf6`.
See `research/artifacts/nf4_14b_remote_execution_20261117.json` for the receipt
and `research/artifacts/nf4_14b_warm_small_audit_20261117.json` for raw checks.
The larger pilot has not been launched.

## Completed paired outcomes

The baseline worker finished in 1655.64 seconds with 95 initialization cache
hits. It retained three files and 20 passing pytest nodes, with stable replay.
There were four candidate-output failures and no unexpected framework errors;
they remain part of the evidence.

| Arm | Module | Retained passing nodes | Lines | Branches | Frozen mutants |
|---|---|---:|---:|---:|---|
| baseline | genty.genty_repeat | 5 | 8/8 = 100% | 2/2 = 100% | 1/1 killed |
| baseline | genty.genty_args | 15 | 18/20 = 90% | 0/0 = NA | no eligible operators |
| improved | genty.genty_repeat | 0 | NA | NA | no stable eligible tests |
| improved | genty.genty_args | 0 | NA | NA | no eligible operators |

The improved worker finished in 2047.70 seconds. Three candidates failed
extraction; three other proposals were accepted by upstream execution but
rejected by the improved assertion-preservation gate. One remaining proposal
was rejected by upstream. This does not prove every rejected oracle was
semantically wrong: repairs changed/deleted assertions or a test and need review.
It does show that the current improved acceptance policy yields no automatically
credited tests in this cohort. Missing coverage is not a measured zero.

The automated `larger_ready=true` in the immutable original summary reflects
framework completion plus a measured baseline path. It does not establish useful
improved output. Our practical decision is **do not expand**. Preserve the
original gate and report this separate quality decision; do not change the old
summary to make the screen appear better.

An independent local audit verified 12 production file hashes, worker exits,
initialization-only cache use, exported rows and raw pytest replay/coverage
numerators and denominators. Baseline used 37 fresh model calls and improved
47; these single-project conditional-warm costs are descriptive.

Source-based review of all three retained files finds constructor/property and
repeat-metadata assertions consistent with production source. The preservation
audit records no removed tests or changed/removed assertion expressions in these
three files. Several constructor/factory cases overlap. No retained args test
exercises `__iter__`; metadata tests for repeat do not establish the surrounding
class-decorator lifecycle. Do not equate 20 nodes with 20 independent behaviors.

Reviewing the improved initial-to-last snapshots explains the preservation
rejections more precisely. Correcting `.args()`/`.kwargs()` to property access
is source-consistent, but the same repairs also remove iteration assertions;
the args repair additionally removes an empty-iteration test. The repeat repair
changes an exception-message assertion and removes the exact repeat-count
assertion in the decorator-chain case. These are mixed repairs, not solely API
corrections. Passing execution alone cannot justify accepting the removed checks.
The rejected wrap proposal even defines a local replacement for `wrap`, rather
than demonstrating correct invocation of the production closure. This motivates
public-API/closure-aware context and explicit oracle review in future variants;
it does not authorize changing this cohort's scores or silently relaxing its gate.

The one repeat mutant changes `count < 0` to `count <= 0`; the zero-count test
detects that boundary change. This is one bounded fault, not broad mutation
efficacy or semantic assertion accuracy. The semantic-accuracy metric remains NA.

The pinned upstream ex1 reference has 100% lines for each of these modules. It
records two args branches, whereas the current raw coverage records zero. The
reference tool version is coverage 7.6.1; current raw metadata says 7.17.3. This
denominator discrepancy blocks direct args branch comparison. No cause is
assumed, and 0/0 must remain NA even though raw coverage displays 100% for an
empty branch denominator. The current one-round, module-owned test scope also
differs from the original artifact conditions. Reference raw JSON is preserved
in `research/artifacts/paper_genty_ex1_reference.json`.

## Subsequent concise-output screen and session change

The `single-test-v1` contract was prepared and verified separately: 159 CPU
tests, 18 focused tests in a fresh exact 79-file overlay, and two real-upstream
orchestration fixtures with scripted model/embedding doubles. Only test
generation/repair prompts change in both arms; initialization and scoring policy
remain fixed. See `docs/KAGGLE_COMPACT_SCREEN.md`.

Driver launch was confirmed for
`UPSTREAM_NF4_COMPACT_20261116T193617595621Z` in the earlier session. Its final
outputs were not retrieved before the old Jupyter endpoint became unreachable.
Its efficacy outcome is **unverified**, not a failed generation score.

The replacement session has an empty working directory and no prepared venv or
cached weights. A fresh preparation/calibration job was launched as
`UPSTREAM_NF4_FRESH_COMPACT_20261117T001507251323Z`. It restores the immutable
earlier real initialization evidence only after source/model/runtime checks;
it prepares new project environments and requires fresh two-T4 memory stress.
It never reuses previous hardware calibration or generated test/scoring outcomes.
A bounded local monitor downloads the final raw ZIP immediately on completion.

The fresh memory calibration passed, including repeated 4096+512 tests on both
T4s with 3.67 GiB conservative headroom. During generation the model continued
to emit complete multi-test modules, rejected by the exact-one-test constraint.
After four baseline and five improved count rejections, only the two study
worker process groups were stopped. The operator-stop receipt records why;
the parent collected all four planned rows as incomplete/NA and blocked larger.
The automatically downloaded ZIP SHA-256 is
`bfe95d801d0f6e8417f2bff8515acb6a308f95447776d665a8698841283774a7`.
This is a development transport failure; it does not establish a quality score.

The user permits a few high-quality selected modules for practical use. These
remain a curated development/application scope; selecting successful modules
does not support an aggregate or representative claim over the paper benchmark.

## Working curated application subset

Two unmodified baseline files were selected for public factory/property and
repeat-metadata/count checks: 12 nodes across two modules. All assertions were
reviewed against pinned production source. Six production hashes were checked,
then three separate fresh-session pytest processes each collected and passed
12/12 nodes with identical node sets. Measured process times: 1.5304, 0.6306,
0.6194 seconds. A separate local Python3.12/pinned-source configuration check
also passed all 12. These are suite replays, not independent model replications;
generation/setup costs are separate.

The original replay archive SHA-256 is
`640262b93035e7b3f5b9cf4aec6ecb4e34915c3466cc5b9a798edee404d78737`.
The runnable package, manifest, replay reports and limitations are under
`research/application/14b_genty_curated_20261117/`; its adjacent ZIP is the
application deliverable. This subset comes from the measured baseline, not
the failed improved/transport experiment. No claims are made for iterator
formatting, complete repeat lifecycle, 7B performance or paper-wide equivalence.
