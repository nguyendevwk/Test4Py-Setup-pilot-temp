---
name: kaggle-dual-gpu-testing
description: Prepare and evaluate Python test generation on Kaggle Dual T4 with traceable execution and research integrity checks.
---

# Kaggle Dual-GPU testing

Prefer maintained repository entrypoints over standalone legacy harnesses. The
presence of a script is not evidence it has been validated on arbitrary projects.
For this repository read `docs/MULTITARGET_SMOKE.md` and the Council skill. Legacy
scripts under this skill require their own validation; do not auto-run campaigns.

1. Use explicit cwd and checked subprocess calls in Python notebook cells.
2. Keep existing CUDA Torch, verify visible devices, record package/model/source
   revisions and measured memory. NF4 is an experimental configuration, not a
   guarantee that every model/prompt fits a T4. Do not claim combined VRAM.
3. Preflight imports and project dependencies before inference. Never silently
   install project dependencies midway through an evaluation or ignore failures.
4. Run a small engineering screen including failure paths, extraction, repair,
   collection, coverage, timeout and replay. A mock does not measure model quality.
5. Preserve every planned attempt and immutable raw evidence. Use fresh outputs,
   keep partial failures and produce archives even if the quality gate fails.
6. Process isolation/timeouts do not constitute a security sandbox. A successful
   setup execution does not establish target reach or valid state for all inputs.
7. Identify curated hints and per-project rules. AST setter prefixes alone do not
   establish automatic, repository-independent state synthesis.
8. No fixed sample count guarantees statistical validity. Attempts within one
   target/project are clustered; lock the design and analyze paired target/project
   outcomes. Never demand a favorable p-value.
9. Pass rate, assertion correctness and fault detection are distinct. Do not
   delete/skip failures or weaken checks to improve scores. Report filtered test
   recovery separately if used; retain pre-filter evidence.
10. Report true line/branch counts, missing values, stage costs and all failure
    denominators. Only claim improvement supported by matched controls. Free API
    usage is not zero compute cost. Never automatically start the full run.

Skill user instructions override any conflicting legacy references or scripts.
