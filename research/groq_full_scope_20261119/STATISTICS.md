# Full eligibility sweep statistics

New full eligibility sweep only; no pooling of prior studies.

Runner accepted boolean: exactly three tests, static gate, all tests pass, target-body witness, and successful same-line replay. The analyzer trusts the runner attestation; aggregate rows cannot independently audit these gates.

Final complete Cartesian product: 3870/3870 attempts; 645 targets; 21 projects.
Equal-project mean of within-project paired target/seed acceptance differences.
Module-line percentage times acceptance; rejected attempts contribute zero, denominator includes every planned attempt. Not target-body coverage.
Primary context_setup-source is separate. Holm correction applies only to the two secondary acceptance p-values; coverage is descriptive.

Bootstrap: 20,000 paired project resamples, seed 20261119. Differences are proportions; line percentages are on a 0–100 scale.

| Contrast | Role | Difference | Marginal 95% CI | Exact two-sided p | Holm p |
|---|---|---:|---|---:|---:|
| context_setup-source | primary | 0.018645 | [-0.01855594145870909, 0.055854173858489696] | 0.346435546875 | not in family |
| verified_setup-source | secondary | -0.030737 | [-0.08722504773758426, 0.010341732971185829] | 0.2858562469482422 | 0.2858562469482422 |
| context_setup-verified_setup | secondary | 0.049382 | [0.0043476456091203, 0.10882789559144823] | 0.0552520751953125 | 0.110504150390625 |

| Arm | Accepted / denominator | Equal-project rate | Equal-project penalized module-line % |
|---|---:|---:|---:|
| source | 378/1290 | 0.351820 | 17.776337 |
| verified_setup | 383/1290 | 0.321084 | 15.220649 |
| context_setup | 423/1290 | 0.370465 | 18.950268 |

| Project | Arm | Accepted / denominator | Penalized module-line % |
|---|---|---:|---:|
| PySnooper | source | 8/34 | 7.353994 |
| PySnooper | verified_setup | 10/34 | 8.998768 |
| PySnooper | context_setup | 8/34 | 6.699365 |
| apimd | source | 5/22 | 4.436971 |
| apimd | verified_setup | 4/22 | 3.362985 |
| apimd | context_setup | 5/22 | 4.350184 |
| codetiming | source | 2/2 | 94.871795 |
| codetiming | verified_setup | 1/2 | 50.000000 |
| codetiming | context_setup | 2/2 | 96.153846 |
| cookiecutter | source | 23/44 | 21.307786 |
| cookiecutter | verified_setup | 27/44 | 24.857027 |
| cookiecutter | context_setup | 31/44 | 28.731792 |
| dataclasses-json | source | 0/16 | 0.000000 |
| dataclasses-json | verified_setup | 1/16 | 3.445122 |
| dataclasses-json | context_setup | 0/16 | 0.000000 |
| docstring_parser | source | 5/50 | 5.894737 |
| docstring_parser | verified_setup | 5/50 | 4.827205 |
| docstring_parser | context_setup | 15/50 | 17.085989 |
| flutes | source | 20/32 | 21.053557 |
| flutes | verified_setup | 17/32 | 17.310002 |
| flutes | context_setup | 19/32 | 21.735468 |
| flutils | source | 27/50 | 21.062217 |
| flutils | verified_setup | 23/50 | 18.545330 |
| flutils | context_setup | 19/50 | 16.358079 |
| httpie | source | 52/180 | 14.339346 |
| httpie | verified_setup | 55/180 | 14.919508 |
| httpie | context_setup | 63/180 | 17.278225 |
| isort | source | 23/32 | 40.494792 |
| isort | verified_setup | 20/32 | 35.069444 |
| isort | context_setup | 19/32 | 33.550347 |
| mimesis | source | 7/22 | 23.860312 |
| mimesis | verified_setup | 6/22 | 15.638210 |
| mimesis | context_setup | 7/22 | 20.888684 |
| py-backwards | source | 9/60 | 10.685748 |
| py-backwards | verified_setup | 8/60 | 9.599606 |
| py-backwards | context_setup | 8/60 | 9.992865 |
| pypara | source | 10/68 | 8.474311 |
| pypara | verified_setup | 12/68 | 10.158884 |
| pypara | context_setup | 13/68 | 10.398591 |
| python-semantic-release | source | 12/20 | 25.091743 |
| python-semantic-release | verified_setup | 10/20 | 20.688073 |
| python-semantic-release | context_setup | 10/20 | 20.688073 |
| python-string-utils | source | 52/84 | 18.794594 |
| python-string-utils | verified_setup | 54/84 | 19.208213 |
| python-string-utils | context_setup | 59/84 | 21.557811 |
| sanic | source | 21/78 | 12.394008 |
| sanic | verified_setup | 23/78 | 15.371630 |
| sanic | context_setup | 29/78 | 19.583098 |
| thefuck | source | 20/92 | 12.556016 |
| thefuck | verified_setup | 22/92 | 14.538684 |
| thefuck | context_setup | 26/92 | 17.332873 |
| tornado | source | 37/138 | 10.454259 |
| tornado | verified_setup | 38/138 | 11.584621 |
| tornado | context_setup | 35/138 | 9.948566 |
| tqdm | source | 7/36 | 7.890212 |
| tqdm | verified_setup | 5/36 | 5.899471 |
| tqdm | context_setup | 9/36 | 9.408243 |
| typesystem | source | 19/90 | 7.789045 |
| typesystem | verified_setup | 24/90 | 10.691222 |
| typesystem | context_setup | 16/90 | 7.571333 |
| youtube-dl | source | 19/140 | 4.497637 |
| youtube-dl | verified_setup | 18/140 | 4.919618 |
| youtube-dl | context_setup | 30/140 | 8.642199 |

Manifest scope: null
Manifest provenance: null

- Projects are assumed independent; shared dependencies and fixed eligibility selection limit generalization.
- Sign-flip inference requires independent project-effect sign exchangeability/symmetry under the null; pairing alone does not establish it.
- Percentile project-cluster bootstrap intervals can have limited coverage with few clusters, discrete outcomes, or heterogeneous projects. They are marginal 95% intervals, not simultaneous intervals.
- Seeds and target symbols are repetitions within projects, not independent project samples. With one project inference is unavailable.
- Acceptance is conditional on the runner oracle and environment; passing generated assertions does not prove semantic correctness or full Test4Py efficacy.
- All 21 projects were already observed; 584 of 645 target symbols were not in the earlier 61 normalized trials. These are not new held-out projects. No older outcomes are pooled.
- No significance, power, or sample sufficiency is promised. Module-line coverage is descriptive, not target-body coverage.

Input SHA-256: {"manifest.json": "155fa962dc8de35777a2399e46f1bdfcb505c52945d0393b59067d7bf5e4edd6", "summary.json": "e65aca649984d7b08e2ec1622da9e748f2fc4b6b565f89826cd2fef759bf4e4c"}
