# Small A/B after the successful 14B memory diagnostic

Open `notebooks/kaggle_14b_small_resume.ipynb` and copy its three Code cells, in
order, into the existing Kaggle session. Do not rerun the old notebook from its
first cell. The previous study, source checkout, venvs, cached weights and
successful diagnostic directories must still exist.

The first cell makes a fresh local Git clone and applies the versioned embedded
source snapshot. It does not modify the earlier checkout. The second freezes a
new 4096/512 plan and validates reuse: project/upstream commits, complete
production inventories and hashes, pip freezes, model/config, diagnostic wrapper
hash, both repeated maximum-context tests and Torch/Transformers/two-T4 profile.
Any mismatch stops the run without installing packages or silently weakening
checks. Calibration identity covers hardware profile/visible slots, not GPU UUID;
the original diagnostic did not record UUIDs.

`stress.json` in the NEW study is explicitly a derived calibration binding.
Original probes/provenance are copied verbatim under `imported-calibration`,
the original diagnostic classification is retained, and no old failed gate is
overwritten. This binding certifies only compatible memory calibration, not
generator or oracle quality. Previously measured GPU cost remains separate.

The third cell runs the actual pinned upstream pipeline with Qwen14B NF4 for
both arms: two genty modules, seed42, one generation round, four module-trials
in two isolated workers. Full production-package initialization/type/RAG remains
real model work; it is not replaced with scripted summaries. The small-only
60-minute budget includes embedding download and model loads. Every failure,
timeout, missing measurement and candidate remains in the evidence. Both arms
share the efficient-attention runtime adaptation.

After completion/failure download the NEW `UPSTREAM_NF4_RESUME_*.zip` for review.
No larger experiment is launched by this notebook. The larger configured pilot
still requires actual small execution/measurement readiness and human review.

Local validation: the three reuse guard tests pass, the supplied real ZIP
settings/probes match the new plan, and a fresh local Git clone plus exact
notebook overlay passed these tests. No GPU generation result is claimed from
this local validation. Prior integrated attention/notebook changes passed 135
CPU tests; no full-suite rerun is demanded on Kaggle for this resume.
