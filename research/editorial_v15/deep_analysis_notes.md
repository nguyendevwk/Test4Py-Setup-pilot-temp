# Independent descriptive analysis for v15

All additional summaries below are **exploratory post hoc**. All 645 targets, 21 projects, three arms and both seeds remain in the analysis (3,870/3,870 attempts). No new significance tests, outcome-based case filtering, repairs or changes to frozen evidence were performed. Existing three-contrast inference is reproduced solely as an audit. No applicable AGENTS.md was found in the repository or ancestor directories.

## Evidence and reproducibility

Run `.venv/bin/python scripts/analyze_v15_descriptive.py`. Raw trial inputs are `research/groq_full_scope_20261119/attempts/*/outcome.json`; every row matches `outcomes.jsonl` and `summary.json` exactly. Target features are parsed from `manifest.json` (AST class/function, setup probe acceptance, nonempty context closure). Raw pack inputs are `joint_packs/main/packs/*/pack_result.json`; every result matches the pack summary, and each pack contains exactly all accepted suites for that project and arm across both seeds. All input paths and SHA-256 digests are in `deep_analysis.json:input_sha256`. All tables below are generated from those raw inputs; JSON keys identify the corresponding calculations.

## Primary contrast: context setup versus source

Among 1,290 target-seed pairs: both accepted **264**, source only **114**, context only **159**, neither **753**. The net gain is 45 accepted attempts; 273 pairs change acceptance. A net gain hides bidirectional turnover. Project outcomes: 9 wins, 5 ties, 7 losses. [JSON: full.contrasts.context_setup-source]

| Arm | Accepted / 1,290 | Pooled % | Equal-project % | Penalized module coverage, equal-project % |
|---|---:|---:|---:|---:|
| source | 378 | 29.3023 | 35.1820 | 17.7763 |
| verified_setup | 383 | 29.6899 | 32.1084 | 15.2206 |
| context_setup | 423 | 32.7907 | 37.0465 | 18.9503 |

## Weighting discrepancy

[JSON: full.contrasts; weighting_decomposition]

- context_setup-source: pooled +3.4884 pp; equal-project +1.8645 pp; 9/5/7 project wins/ties/losses.
- verified_setup-source: pooled +0.3876 pp; equal-project -3.0737 pp; 10/1/10 project wins/ties/losses.
- context_setup-verified_setup: pooled +3.1008 pp; equal-project +4.9382 pp; 13/2/6 project wins/ties/losses.

This is a change of estimand: pooled rates weight projects by target counts; the primary estimand weights every project equally. For codetiming, one target gives two pairs: verified setup loses one acceptance, a -50 pp project effect and a -2.3810 pp contribution to the 21-project mean, versus -0.0775 pp to the pooled mean. Keep that project in all analyses; explain the leverage rather than deleting it. The decomposition records every project contribution.

## Complete project results

[JSON: per_project; differences in percentage points]

| Project | Targets | Source accepted | Verified accepted | Context accepted | Context-source pp |
|---|---:|---:|---:|---:|---:|
| PySnooper | 17 | 8 | 10 | 8 | +0.0000 |
| apimd | 11 | 5 | 4 | 5 | +0.0000 |
| codetiming | 1 | 2 | 1 | 2 | +0.0000 |
| cookiecutter | 22 | 23 | 27 | 31 | +18.1818 |
| dataclasses-json | 8 | 0 | 1 | 0 | +0.0000 |
| docstring_parser | 25 | 5 | 5 | 15 | +20.0000 |
| flutes | 16 | 20 | 17 | 19 | -3.1250 |
| flutils | 25 | 27 | 23 | 19 | -16.0000 |
| httpie | 90 | 52 | 55 | 63 | +6.1111 |
| isort | 16 | 23 | 20 | 19 | -12.5000 |
| mimesis | 11 | 7 | 6 | 7 | +0.0000 |
| py-backwards | 30 | 9 | 8 | 8 | -1.6667 |
| pypara | 34 | 10 | 12 | 13 | +4.4118 |
| python-semantic-release | 10 | 12 | 10 | 10 | -10.0000 |
| python-string-utils | 42 | 52 | 54 | 59 | +8.3333 |
| sanic | 39 | 21 | 23 | 29 | +10.2564 |
| thefuck | 46 | 20 | 22 | 26 | +6.5217 |
| tornado | 69 | 37 | 38 | 35 | -1.4493 |
| tqdm | 18 | 7 | 5 | 9 | +5.5556 |
| typesystem | 45 | 19 | 24 | 16 | -3.3333 |
| youtube-dl | 70 | 19 | 18 | 30 | +7.8571 |

## Terminal failure categories

These are terminal runner labels, not causal diagnoses or conditional stage probabilities. Collection failures may be included in test_failure; no finer failure category is fabricated. [JSON: full.arms.*.status_counts and full.contrasts.*.terminal_status_transition_counts]

| Status | Source | Verified | Context |
|---|---:|---:|---:|
| completed | 378 | 383 | 423 |
| execution_timeout | 3 | 2 | 5 |
| extraction_failure | 16 | 15 | 13 |
| quality_gate_failed | 52 | 47 | 49 |
| target_not_reached | 29 | 28 | 43 |
| test_failure | 812 | 815 | 757 |

The following mutually exclusive refinement retains the full planned denominator. For terminal test_failure, inspect eval0/pytest.json with precedence: failed collector, failed setup/teardown, failed test call, other reported, unavailable report. Mixed failures are assigned by this precedence, not counted twice. These describe where pytest failed, not the semantic root cause. [JSON: stage_failure_partition; stage_failure_records, including raw report paths]

| Stage partition | Source | Verified | Context |
|---|---:|---:|---:|
| completed | 378 | 383 | 423 |
| execution_timeout | 3 | 2 | 5 |
| extraction_failure | 16 | 15 | 13 |
| quality_gate_failed | 52 | 47 | 49 |
| target_not_reached | 29 | 28 | 43 |
| test_failure:call_failed | 720 | 730 | 669 |
| test_failure:collection_failed | 84 | 75 | 65 |
| test_failure:setup_or_teardown_failed | 8 | 10 | 23 |

## Exhaustive subgroup summaries

All strata retain both seeds and all arms, including failed attempts. Equal-project means balance only projects represented within that stratum; varying project composition and correlated target attributes prevent causal subgroup or interaction conclusions. Closure availability is supplementary descriptive context. The setup-by-kind cross-tab partitions all targets exactly. No subgroup p-values or confidence intervals are computed. [JSON: subgroups]

| Stratum | Targets | Projects | Source accepted | Verified accepted | Context accepted | Context-source pooled pp | Context-source balanced pp | Verified-source balanced pp |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| setup_available:False | 308 | 19 | 193 | 186 | 223 | +4.8701 | +3.9920 | -1.5422 |
| setup_available:True | 337 | 21 | 185 | 197 | 200 | +2.2255 | +2.7513 | -1.9526 |
| kind:class | 288 | 20 | 118 | 127 | 133 | +2.6042 | +0.5407 | -3.9221 |
| kind:function | 357 | 18 | 260 | 256 | 290 | +4.2017 | +3.2099 | -0.4941 |
| closure_available:False | 257 | 21 | 156 | 157 | 160 | +0.7782 | +0.5088 | -2.0830 |
| closure_available:True | 388 | 20 | 222 | 226 | 263 | +5.2835 | +3.7978 | -0.8608 |
| setup_by_kind:setup=False;kind=class | 52 | 13 | 21 | 17 | 17 | -3.8462 | +2.9762 | +3.1177 |
| setup_by_kind:setup=False;kind=function | 256 | 18 | 172 | 169 | 206 | +6.6406 | +5.7038 | -0.7087 |
| setup_by_kind:setup=True;kind=class | 236 | 20 | 97 | 110 | 116 | +4.0254 | +2.3197 | -0.3375 |
| setup_by_kind:setup=True;kind=function | 101 | 15 | 88 | 87 | 84 | -1.9802 | -4.0564 | -0.4251 |

Unavailable setup does not imply a setup intervention was delivered. Residual arm differences in identical-prompt strata can arise from generation/execution variation; they do not establish a setup mechanism. Availability itself is not randomized.

## Seed sensitivity

[JSON: by_seed; seed_stability; context_source_target_delta_seed71_seed72]

| Seed | Source accepted | Verified accepted | Context accepted | Context-source pooled pp | Context-source balanced pp | Verified-source balanced pp |
|---|---:|---:|---:|---:|---:|---:|
| 71 | 183 | 198 | 207 | +3.7209 | +1.8982 | -4.7124 |
| 72 | 195 | 185 | 216 | +3.2558 | +1.8308 | -1.4349 |

- source: 132 targets accepted on both seeds; 114 on exactly one; 399 on neither.
- verified_setup: 128 targets accepted on both seeds; 127 on exactly one; 390 on neither.
- context_setup: 151 targets accepted on both seeds; 121 on exactly one; 373 on neither.

The combined equal-project effect is the arithmetic mean of the two seed-specific effects because each project has the same target frame at both seeds. Two seeds do not establish robustness across generation settings, and are not independent projects.

## Standalone acceptance versus joint-pack usability

This audit was added after generation began and remains supplementary exploratory. It combines every accepted suite across both seeds without editing. Failure of one test can invalidate a whole pack; the selected test count differs by arm. Higher standalone acceptance therefore need not imply better integration. [JSON: joint_pack_summary; joint_pack_details]

| Arm | Passing packs / 21 | Nonempty failed projects | Expected / collected nodes | Available measured projects | Measured available-case coverage % | Validated coverage, all 21 % |
|---|---:|---|---:|---:|---:|---:|
| source | 20 | none | 1134 / 1134 | 20 | 52.6336 | 50.1273 |
| verified_setup | 18 | flutes, mimesis, tornado | 1149 / 1149 | 21 | 51.8699 | 44.3646 |
| context_setup | 17 | tornado, thefuck, python-semantic-release | 1269 / 1269 | 20 | 54.2030 | 44.9780 |

An empty pack counts as nonpassing, not as an executed failure. Source and context each have an empty dataclasses-json pack; verified setup has no empty pack. All expected nodes were collected, which does not imply that all nodes passed. Validated pack coverage is zero for nonpassing/empty packs. Available-case measured coverage excludes missing measurements and can include coverage from failing packs; it must not replace the all-project validated measure. Standalone and pack coverage use different denominators and cannot be interpreted as a common treatment effect. The result supports an integration/usability limitation, not an identified cause or proof that more context intrinsically harms integration.

## Independent check of the existing inference

Project effects were recomputed from individual outcome booleans. Exact sign-flip probabilities were recomputed using rational effects scaled to a common integer denominator and an integer subset-sum distribution, independent of the frozen floating-point sign enumeration. The original 20,000 project bootstrap draws and two-secondary Holm adjustment were reproduced. This verifies arithmetic, not the inferential assumptions. [JSON: existing_statistics_independent_verification; existing_secondary_holm_verified]

| Existing contrast | Balanced effect pp | Original bootstrap 95%, pp | Exact p | Secondary Holm p |
|---|---:|---|---:|---:|
| context_setup-source | +1.864505 | [-1.855594, 5.585417] | 0.346435547 | outside secondary family |
| verified_setup-source | -3.073674 | [-8.722505, 1.034173] | 0.285856247 | 0.285856247 |
| context_setup-verified_setup | +4.938179 | [0.434765, 10.882790] | 0.055252075 | 0.110504150 |

The primary interval includes zero and the exact primary p-value does not support a superiority claim. The context-versus-verified marginal bootstrap interval excludes zero while the exact p exceeds .05 and its Holm-adjusted p is about .111: different procedures can disagree. Do not promote that marginal interval to multiplicity-controlled evidence. Sign-flip inference needs independent project-effect sign exchangeability/symmetry; bootstrap calibration is limited with 21 heterogeneous, previously observed projects. Passing generated tests is not independent semantic oracle validation or full Test4Py efficacy.

## Actionable editorial conclusions

1. Lead with the prespecified equal-project primary effect and its uncertainty; show pooled counts as descriptive support, with the full paired turnover table.
2. Explain the verified-setup pooled/balanced sign reversal using unequal project weights and the complete contribution decomposition. Do not remove codetiming or redefine the primary estimand.
3. Present setup availability, class/function and their complete cross-tab as hypothesis-generating descriptions, with denominators and represented-project counts; avoid subgroup superiority claims.
4. Place standalone acceptance and joint-pack usability side by side, and distinguish empty packs, failing nonempty packs, measured coverage availability, and validated coverage over all projects.
5. State that all projects were previously observed and two seeds repeat targets within projects. Independent assertion review, mutation/real-fault validation and a prospective held-out-project evaluation remain necessary for stronger efficacy claims.
