**Reproducibility record — Council study, 18–19 November 2026**

The original DOCX and historical data were not edited. New reports are copies
with corrected tables and separately identified new cohorts. A zip checksum
manifest binds each included evidence file to its exact bytes.

**What can be reproduced**

- Recompute all new counts from saved attempt outcomes and pytest/coverage JSON.
- Replay the exact saved generated code on the saved subject source, with the
  recorded Python and dependency versions. New files must be used for replays.
- Recompute project-cluster bootstrap and exact sign-flip statistics using the
  saved statistical script and seed. No API is needed for these operations.
- Regenerate corrected charts/DOCX from the included builder and evidence.

Fresh provider inference is not guaranteed byte-identical even with the same
API seed. The provider exposes a model alias, not an immutable weight SHA.
Raw requests, responses, usage, finish reasons and available fingerprints are
saved; this supports auditing actual inference, not a false determinism claim.
Source-based assertion review is not independent specification validation.

**Cohorts and scope**

1. Restored historical data: original 96/105; after refinement 98/105. The latter
   is a mixed development cohort with target tuning; original and rerun artifacts
   are retained. Ablation is 5/6. Missing provenance is documented, not invented.
2. New pilot: 54 attempts, nine targets/three projects, source vs bounded AST
   dependencies. Recovery and selected-subset mutation are secondary endpoints;
   original suite outcomes are unchanged by filtering.
3. Post-pilot development: 36 attempts on those same targets, two atomic arms.
   This is development, not fresh held-out confirmation.
4. Expanded component evaluation: 162 attempts, 27 targets/nine eligible projects,
   three repetitions/two arms. Ten candidate projects were fixed before inference;
   black's three target slots were excluded before model outcomes because the
   import loader resolved to compiled .so modules; adjacent .py files do exist.
   The preparer accepted only .py import origins and did not force source loading.
   SOURCE_ELIGIBILITY_CORRECTION.json clarifies the original manifest wording;
   no original run evidence or completed outcome was changed. All eligible
   attempts, including failures, remain.
   Current resolved PyPI versions differ from paper commits. This is not the full
   Test4Py upstream and cannot establish superiority over the paper.

5. Output-cap engineering screen:108 attempts on the already observed27 targets,
   seed45; caps1536/2048. This is operational sensitivity, not independent efficacy.
6. Published CodaMOSA module-frame adaptation:204 attempts,34 targets/12 projects,
   three seeds/two arms. Fixed candidates and source-only selection preceded inference;
   resolved PyPI versions are pinned, not original Docker commits. These12 projects
   do not overlap prior Groq cohorts, but four were used in historical105-target
   development. HISTORICAL_OVERLAP_DISCLOSURE.json records this; eight projects
   extend beyond both those scopes. All204 outcomes remain in the primary comparison.
   A CRLF text-vs-byte hash check correction preserved all six completed first-target
   outcomes. One unclosed-code-fence response remains a failure; derived analysis
   classifies its raw error:ValueError as quality_gate_failed, with unchanged false
   acceptance and a reproducible extraction diagnostic. Originals remain unchanged.
   Original prospective analysis is in scripts/analyze_groq_codamosa_extension.py;
   finalized output uses analysis_inputs/ plus ANALYSIS_STATUS_CLASSIFICATION.json.
   Recompute in a copied workspace with:
   `python scripts/recompute_groq_extension.py`
   This consumes audited analysis_inputs and writes derived statistics there,
   preserving original outcomes and original summary.json.
7. Context-closure development:68 attempts on those same34 observed targets, seed46,
   source vs bounded AST helper/global declarations plus available setup. No repair,
   no pruning.11/34 vs12/34;23 accepted artifacts replayed. This is not held-out proof.

The six Groq cohorts contain632 model attempts. They must not be pooled into632
independent projects. Cumulative ledger response counts differ because other
previous requests and infrastructure history are separately accounted.

**Retained14B execution and reusable tests**

The real Qwen2.5-Coder-14B NF4 Kaggle stage remains documented: memory adaptation,
4/4 stress checks, cold timeout with missing scoring (NA), warm completion with20
baseline nodes, and the negative improved-arm gate outcome.59 structural raw
execution files from three hash-verified historical archives are included.
The12-test curated baseline replays12/12 in each of three new CPU processes.
The historical14-test extension preserves all12 old tests and adds two verbatim
model tests: three new processes pass14/14; genty_args lines18/20 become20/20;
args branches0/0 are NA. Two historical posthoc iterator mutants survive old12
and are assertion-killed by new14 on the same pinned source. This is a selected
application benefit, not a held-out real-fault or full algorithm efficacy claim.

```sh
python scripts/replay_14b_application.py --output /tmp/new-14b-baseline-replay
python scripts/replay_14b_extended_application.py --output /tmp/new-14b-extended-replay
```

Use a new output path for every replay; existing evidence directories are preserved.
No new model inference is involved. Source and test hashes are checked.

The provider gateway incident is separately preserved (54 non-model responses,
HTTP gateway 1010); it is not a model-quality experiment. An interrupted unfinished
expanded attempt is retained under interrupted_attempts; no completed result was
replaced when resuming the same locked plan.

**Verify and derive a portable replay workspace**

From an extracted archive root (contains scripts/, research/, repro/):

```sh
python3 scripts/package_council_repro.py --verify /absolute/path/council_repro_20261119.zip
python3 scripts/package_council_repro.py --root "$PWD" --restore-root /tmp/council-replay
```

Restore remaps absolute paths only in derived manifests/summaries. The original
zip evidence remains unchanged; derived JSON has different hashes and is marked
by RELOCATION.json. Use Python 3.10 for model-test replays, as recorded. The
restore helper requires a Python with tarfile's safe `filter='data'` support.

Each `repro/environments/PROJECT/requirements.txt` pins all resolved packages for
that project. Create separate environments to avoid dependency conflicts:

```sh
cd /tmp/council-replay
uv venv --python 3.10 /tmp/council-apimd-env
uv pip install --python /tmp/council-apimd-env/bin/python -r repro/environments/apimd/requirements.txt
/tmp/council-apimd-env/bin/python scripts/replay_groq_study.py research/groq_confirmation_20261118 --project apimd --output-root /tmp/council-apimd-new-replay
```

Repeat per project using the corresponding environment and a fresh output root.
The saved subject package is prepended to PYTHONPATH; pinned environment packages
provide its dependencies. Runtime versions and subject-source hashes are recorded
in repro/environments/PROJECT/versions.json. Confirm source hashes before replay.
No API key or network is needed once dependencies are installed. Test subprocesses
receive a minimal environment without user/API credentials; this is process
isolation, not a security sandbox. Review generated code before executing it.

To recompute statistics without inference:

```sh
uv run --no-project --python 3.10 --with numpy==2.2.6 scripts/analyze_groq_confirmation_statistics.py --study research/groq_confirmation_20261118
```

Recomputation writes derived statistics files; perform it in a copied replay
workspace. Other commands use `--help` for optional paths. Recreating new API
campaigns requires a fresh plan/output and an explicitly tracked cumulative cap;
do not accidentally regenerate results just to audit them.

**Budget**

The cap is USD 3 cumulative. The latest research/groq_context_development_20261119/budget.json separates settled configured-price
usage estimates, uncertain reservations and the user's USD 0.50 opening allocation.
The opening allocation is a conservative budget reconciliation, not fabricated
API usage or an invoice. Never add token estimates to console spend as though
they are distinct measured bills. Safe rate-limit headers and retry-after values
are retained; the client runs serially and does not retry an uncertain charge.

**Statistical limitations**

There are nine project clusters in the original expanded component evaluation, not162
independent projects. The later extension has12 project clusters, not204. Project-wise resampling is used. The observed gain is not
a promise of significance; the reported 95% cluster interval includes zero.
Source eligibility and project selection limit generalization. Prior development,
secondary recovery and selected mutant screens are not pooled into a larger
independent efficacy sample. Equivalent mutants and real-fault detection are not
established by a small syntactic mutation screen.

Latest report: reports/Tieu_Luan_CNPMTT_Council_SOTA_v10.docx and rendered PDF. Earlier versions and original remain preserved.
