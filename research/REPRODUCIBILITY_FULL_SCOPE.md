Full-scope Council component evaluation, 19 November 2026

The complete eligibility frame contains645 public functions/classes across169 modules and21 already-observed projects. All645 are evaluated with three arms and seeds71/72:3870 model cases,1290 per arm. The arms are source, source+verified setup, and source+verified setup+bounded same-module declarations. No repair or outcome-based case filtering is used.

This is the entire stored eligibility frame, not a complete original Test4Py pipeline replication or new-project held-out test.584 targets were not in the earlier61-target normalized evaluations; all21 projects were already observed. Published module frames are adapted to pinned resolved package versions.

The primary contrast is context_setup-source. Two secondary contrasts isolate setup and declaration closure; Holm correction is applied only to these secondary p-values. Analysis requires the entire planned Cartesian product. Bootstrap uses20000 paired project resamples with seed20261119. Exact sign-flips use project clusters, not independent API-call assumptions. No statistical significance or oracle correctness is guaranteed.

Every response, generated code, pytest report, coverage JSON and terminal outcome is retained. Signals, corrupt evidence and uncertain provider failures interrupt rather than becoming model-quality failures. Timeout20s is an operational endpoint. Three top-level test functions must be collected; parametrized nodes remain inside those functions. All accepted suites have a same-coverage replay and target-body witness; independent replay is a separate secondary audit and does not rewrite primary accepted flags.

Verify the old v4 evidence bundle and the new supplemental bundle before extraction. The supplemental repro/FULL_SCOPE_BASE.json records the required old bundle SHA256. Extract the v4 bundle into a new directory, then overlay the supplemental files. Original archives remain unchanged. The new shared ledger is an append-only extension of the old ledger.

```sh
python scripts/package_council_repro.py --verify /path/council_repro_20261119_v4.zip
python scripts/package_groq_full_scope.py --verify /path/council_full_scope_20261119_v1.zip
```

Compute full-scope statistics offline in a copied workspace with Python3.10 and numpy2.2.6:

```sh
python scripts/analyze_groq_full_scope.py --study research/groq_full_scope_20261119
```

For a portable independent replay, install one project's recorded requirements from repro/environments/PROJECT/requirements.txt into a fresh Python3.10 environment. Project source from that installation must match each original raw source hash. Then replay that project explicitly:

```sh
python scripts/replay_groq_full_scope.py --study research/groq_full_scope_20261119 --project codetiming --python /tmp/codetiming-env/bin/python --output-root /tmp/new-codetiming-audit
```

Use a separate environment for each project. Without --python, replay uses the original pinned local environments. --project produces an explicitly selected subset audit, not a full-study audit. All official accepted outcomes can be replayed using the recorded project environments and a fresh output root. Completed replay results remain immutable; interruption artifacts are kept.

The report is built from reports/Tieu_Luan_CNPMTT_Council_SOTA_v12.docx, the v11 reference bank, and research/editorial_v13/report_body.md. Both inputs are preserved. The completed numerical substitution is in resolved_values.json, and evidence hashes are provided separately. Model aliases and API seeds do not guarantee fresh inference is byte-identical. Exact saved-code replay and deterministic statistics support audit without new paid calls.

Budget uses one cumulative3USD ledger. Usage prices are estimates, not invoices. Conservative allocations include unresolved reservations and the reported opening allocation; do not add these to token estimates as separate bills. Serial provider requests obey account rate headers. Cached token billing may be lower than configured uncached-price estimates.
