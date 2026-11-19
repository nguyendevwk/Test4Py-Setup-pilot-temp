# Confirmation statistics

Post-hoc analysis of completed confirmation only; no pilot/development pooling.

9 project clusters; 27 targets; 81 paired target/seed repetitions.
Primary comparison: ITT-style assignment contrast across all eligible targets, regardless of probe acceptance; post-hoc statistical plan.
Independent unit: project. Contrast: verified setup minus source. Acceptance is the unchanged runner endpoint.

Equal-project acceptance difference: 0.0988; 95% percentile cluster bootstrap CI [-0.0123, 0.2222].
Equal-project relative risk: 1.2857; 95% cluster bootstrap CI [0.9630, 1.8400].
Undefined RR bootstrap draws: 0/20000. NA when source rate is zero; CI NA if any bootstrap denominator is zero.
Exact two-sided project sign-flip p: 0.2188 (512 sign assignments).
Exact enumeration under independent project-effect sign exchangeability/symmetry under null; not guaranteed by pairing alone.
Bootstrap: 20,000 paired project resamples; deterministic seed 20261118. Effects are proportions (multiply differences by 100 for percentage points).

## Arms (descriptive)

| Arm | Accepted / attempts | Rate | Wilson 95% |
|---|---:|---:|---|
| atomic_source | 28 / 81 | 0.3457 | [0.2512, 0.4541] |
| atomic_verified_setup | 36 / 81 | 0.4444 | [0.3412, 0.5527] |

Wilson intervals ignore clustering and must not be used as cluster-aware inference.

## Project results

| Project | Pairs | Source | Verified | Difference | RR | Verified only | Source only | Missing |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| apimd | 9 | 0.1111 | 0.0000 | -0.1111 | 0.0000 | 0 | 1 | 0 |
| dataclasses-json | 9 | 0.0000 | 0.0000 | 0.0000 | NA | 0 | 0 | 0 |
| flutes | 9 | 0.3333 | 0.3333 | 0.0000 | 1.0000 | 0 | 0 | 0 |
| httpie | 9 | 0.6667 | 0.8889 | 0.2222 | 1.3333 | 2 | 0 | 0 |
| isort | 9 | 0.7778 | 0.6667 | -0.1111 | 0.8571 | 2 | 3 | 0 |
| mimesis | 9 | 0.2222 | 0.6667 | 0.4444 | 3.0000 | 4 | 0 | 0 |
| py-backwards | 9 | 0.3333 | 0.3333 | 0.0000 | 1.0000 | 0 | 0 | 0 |
| pypara | 9 | 0.0000 | 0.2222 | 0.2222 | NA | 2 | 0 | 0 |
| python-semantic-release | 9 | 0.6667 | 0.8889 | 0.2222 | 1.3333 | 3 | 1 | 0 |

Discordant/concordant counts: {"discordant_verified_only": 13, "discordant_source_only": 5, "both_accepted": 23, "neither_accepted": 40}

Missingness and pre-inference exclusions: {"planned_attempts": 162, "observed_attempts": 162, "missing_attempts": 0, "expected_target_slots": 30, "pre_inference_missing_target_slots": 3, "scope": "Excluded project/target slots are not model failures; inference covers eligible projects only."}

Per-project terminal status counts are included in statistics.json.

## Prospective sample-size sensitivity (assumptions only)

| Difference | Discordance | ICC | Pairs/project | Independent pairs approx. | Projects with design effect approx. |
|---|---:|---:|---:|---:|---:|
| 0.05 | 0.25 | 0.00 | 9.0 | 778 | 87 |
| 0.05 | 0.25 | 0.10 | 9.0 | 778 | 156 |
| 0.05 | 0.25 | 0.30 | 9.0 | 778 | 294 |
| 0.05 | 0.50 | 0.00 | 9.0 | 1562 | 174 |
| 0.05 | 0.50 | 0.10 | 9.0 | 1562 | 313 |
| 0.05 | 0.50 | 0.30 | 9.0 | 1562 | 591 |
| 0.10 | 0.25 | 0.00 | 9.0 | 189 | 21 |
| 0.10 | 0.25 | 0.10 | 9.0 | 189 | 38 |
| 0.10 | 0.25 | 0.30 | 9.0 | 189 | 72 |
| 0.10 | 0.50 | 0.00 | 9.0 | 385 | 43 |
| 0.10 | 0.50 | 0.10 | 9.0 | 385 | 77 |
| 0.10 | 0.50 | 0.30 | 9.0 | 385 | 146 |
| 0.15 | 0.25 | 0.00 | 9.0 | 80 | 9 |
| 0.15 | 0.25 | 0.10 | 9.0 | 80 | 16 |
| 0.15 | 0.25 | 0.30 | 9.0 | 80 | 31 |
| 0.15 | 0.50 | 0.00 | 9.0 | 167 | 19 |
| 0.15 | 0.50 | 0.10 | 9.0 | 167 | 34 |
| 0.15 | 0.50 | 0.30 | 9.0 | 167 | 64 |

## Pre-inference intervention deliverability (exploratory)

Manifest setup_probe.accepted, measured before model inference; never selected from model outcomes.
Probe acceptance measures intervention deliverability. When false, no setup hint is appended: treatment and control prompt content are identical; generation seed/order do not constitute a hint intervention.
Within each stratum, target/seed pairs are averaged within project, then projects weighted equally. Stratum effects need not average to the full ITT effect.

| Probe stratum | Targets | Projects | Pairs | Difference | Cluster 95% CI | RR | RR 95% CI | Sign-flip p |
|---|---:|---:|---:|---:|---|---:|---|---:|
| probe_accepted_delivered | 18 | 9 | 54 | 0.1481 | [0.0000, 0.3333] | 1.5333 | [1.0000, 2.4286] | 0.2500 |
| probe_failed_no_hint | 9 | 5 | 27 | 0.0333 | [-0.1000, 0.2000] | 1.0833 | NA | 1.0000 |

Full stratum arms, discordance, per-project results and status counts are in statistics.json. Empty or single-project strata do not support cluster inference.

## Project selection and scope

Ten fixed candidate projects, nine eligible under the recorded import-origin criterion. black contributes three pre-inference target slots: loader origins resolve to compiled .so modules, although adjacent .py source files exist. The preparer accepted only .py import origins; it did not force source loading or measure compiled-code coverage. Exclusion preceded model outcomes; do not describe this as absence of source. The original manifest wording is clarified by SOURCE_ELIGIBILITY_CORRECTION.json.
Component evaluation using resolved PyPI releases, not the complete Test4Py method or original pinned-paper replication; no full-paper efficacy claim.

## Budget reconciliation context

Cumulative authorized budget: USD 3. User-reported opening balance: USD 0.50. These are reconciliation context, not API usage or measured spend.

## Limitations

- Post-hoc statistical analysis, not a prospectively registered inference plan.
- Nine project clusters give limited precision; percentile bootstrap may be poorly calibrated.
- Project selection and shared ecosystem dependencies limit generalization and independence.
- Wilson intervals and raw discordance counts are descriptive; no independent-pair p-value.
- Sensitivity uses paired binary normal approximation, alpha .05 two-sided, power .80, assumed discordance and exchangeable within-project ICC.
- Design-effect project counts are approximate, with balanced cluster size assumed; not a small-cluster power calculation.
- No guaranteed significance, observed-power claim, or proof that this sample is sufficient.
- Delivered-stratum analyses are exploratory, without multiplicity adjustment; no full-paper efficacy claim.
