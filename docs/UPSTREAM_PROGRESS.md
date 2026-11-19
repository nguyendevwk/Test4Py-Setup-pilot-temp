# Upstream progress and terminal outcomes

Progress is measured work counts, not a percentage of runtime or a quality score.

| Stage | Display | Meaning |
|---|---|---|
| Model load | elapsed / remaining budget | No guessed load percentage |
| Initialization | step x/11 and items n/N | Separate function/class items and CPU embedding index |
| Generation | round r/R, functions n/N, current function/operation | Functions processed, including errors or already-covered functions |
| Scoring | modules n/N and mutants m/M | Scoring work processed, not mutants killed |
| Scheduler | workers finished n/N | Terminal workers, including failures |
| Model calls | calls finished, total dynamic | Repair/type/retrieval calls make the final total unknown |

Example heartbeat:

```text
[progress:genty-42-improved] elapsed=900s remaining<=2700s |
generation_round_1 | round=1/1 | functions=[#####-------] 3/7 |
GentyArgs.kwargs | operation=repair_assert_error |
calls_finished=118 (total dynamic)
```

Initialization uses the upstream tqdm item updates without changing method return
values or task ordering. CPU function-database indexing, previously outside the
ten tracked project methods, is now the 11th tracked step. A separate ready event
marks successful return from project.init. Structural boundaries and live
heartbeats remain visible after the compact model-event display limit.

A worker killed by the deadline can leave report.json with status=running.
Parent collection derives terminal timeout from process.json. Placeholder module
rows are reported separately from completed trials. If no retained suite has
been measured, its pass rate is NA; observed-success/planned bookkeeping is a
separate field. No missing coverage is converted to zero.

## Resource admission

Future paired CLI runs check current free VRAM and acquire cooperative locks
using physical GPU UUIDs before loading models. The 14B profile requires at least
12.5 GiB free per selected GPU at admission. Busy/reserved GPUs cause an explicit
preflight stop; no process is killed and no model is silently changed. This does
not reserve resources against unrelated programs that ignore these locks.
OOM inside the model constructor is also classified as a hardware-budget failure,
even when no model-call log could be created.

## Exact initialization reuse

Only completed greedy initialization outputs may be imported from a prior run.
The importer verifies full prompt/cache keys, raw outputs, model/embedding
revisions, runtime, production-source inventory and settings. Changed incoming
prompts naturally miss the cache. New code fingerprints and old/new key mappings
are recorded. No generation, repair, test, coverage or mutant result is reused.
All original outputs, including cap hits, remain unchanged and cold cost stays
in the original run. A warm-prefix retry is not evidence of cold one-hour runtime.
