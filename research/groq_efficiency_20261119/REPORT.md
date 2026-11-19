**Output-cap engineering screen — 19/11/2026**

Fixed27previously observed targets,9projects,2contextarms,2outputcaps,onebest-effortseed45,108planned/completedattempts. Same3testfunction requirement, source/model, quality gate, target witness and replay; zero repair. This is operational sensitivity, not new independent efficacy confirmation.

| Arm | Cap | Accepted/27 | Penalized module SC | Output tokens | Limit hits | Mean total seconds |
|---|---:|---:|---:|---:|---:|---:|
|atomic_source|1536|13/27|24.12%|12521|0|3.381|
|atomic_source|2048|14/27|26.52%|12584|0|3.540|
|atomic_verified_setup|1536|9/27|15.74%|14300|0|3.143|
|atomic_verified_setup|2048|10/27|18.24%|12855|0|3.162|

No response reached either output cap. Lower cap did not save observed tokens overall or improve acceptance. Retain2048 as a practical margin, not proof of optimality. Differences are stochastic and the screen has only one repetition/cell. The setup arm does not consistently outperform control here; preserve this alongside the earlier positive-but-inconclusive effect.

Total seconds includes API pacing/network plus local pytest/replay. Do not compare these directly with14B Kaggle cold costs or call them kernel-only latency. Full requests/responses and cost allocation are in the shared ledger and budget.json.
