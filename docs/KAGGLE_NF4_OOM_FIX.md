# Kaggle 14B NF4 stress failure — 2026-11-17

Input evidence: `notebook1aa30d2af4.ipynb` and
`UPSTREAM_NF4_20261116T170358791891Z.zip`. Immutable input hashes and probe
records are in [the audit](../research/artifacts/upstream_nf4_20261116_gpu_audit.json).

## Observed cause

131 source tests passed on Kaggle. Both target environments and scripted fixtures
completed. Both T4s loaded Qwen2.5-Coder-14B NF4 (~9.29 GiB allocated).
Both passed 2048 input + 512 forced output tokens: peak allocated ~11.34 GiB,
conservative margin ~2.90 GiB. Both failed on 4096 input in PyTorch SDPA with
CUDA OOM: allocation request 2.50 GiB, available 1.65 GiB. No permission denial
or root policy rejection appears in the supplied notebook. `ROOT` denotes the
study folder under `/kaggle/working`, not the Linux `/root` directory.

## Runtime correction

New common policy `t4-efficient-sdpa-v1` selects Transformers' existing explicit
KV-head repetition path and PyTorch `EFFICIENT_ATTENTION` for CUDA generation.
Transformers 4.57.6 can otherwise request native GQA; PyTorch 2.11 documents
native GQA support in flash/math kernels, while T4 cannot use FlashAttention-2.
The observed OOM allocation is consistent with the quadratic math path. Kernel
dispatch was not traced in the old run, so that path attribution remains an
inference; CUDA OOM itself is confirmed.

This is a shared runtime adapter, not an experimental treatment advantage.
It changes floating-point kernel execution, which can change exact outputs;
never merge this new cohort with old runtime measurements. Model/weights,
4096/512 budgets, quantization, headroom threshold and outcomes remain unchanged.
CPU embeddings retain normal kernel selection. Unsupported efficient kernels
fail closed; there is no silent CPU, math, model or context-size fallback.

## Notebook behavior

Install uv in a dedicated venv using pip's `--python`, rather than modifying
Kaggle's system Python. Existing CUDA Torch is retained. No sudo, privilege
escalation, background keepalive, quota bypass or external remote server is added.
Notebook work uses `/kaggle/working` outputs and temporary venvs. Internet and GPU
are normal user-selected Kaggle settings. See [Kaggle notebooks documentation](https://www.kaggle.com/docs/notebooks)
and [Acceptable Use Policy](https://www.kaggle.com/aup); code review does not certify
account-specific permissions or platform enforcement decisions.

Stress failures print probe status, measured headroom and exact errors directly.
A failed step latches the notebook runner and prevents later subprocess launches.
The original evidence is preserved; run the corrected source in a fresh output
because the source/plan fingerprints changed. The larger stage stays disabled.

## Validation boundary

CPU tests can check HF repeat_kv numerical equivalence, context selection,
venv-targeted pip and failure latching. They cannot establish T4 kernel
availability or prove 4096-token VRAM fit. The corrected Kaggle stress must pass
before real generation or the larger stage is admitted.
