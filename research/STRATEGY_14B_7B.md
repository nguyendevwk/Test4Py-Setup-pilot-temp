# Strategy: practical small-model regression testing

Decision date: 2026-11-17, Asia/Ho_Chi_Minh.
User objective: a practical pipeline approaching or exceeding the original
paper's results with 14B, preferably 7B, and a reliable small screen before
expensive expansion. All decisions must have an evidence-based rationale.

## What counts as success

Use three separate conclusions:

1. **Engineering readiness:** the planned jobs finish, source/model identities
   match, no unresolved infrastructure error or resource-budget violation exists,
   and raw pytest/replay/coverage measurements agree with exported records.
2. **Useful tests:** tests reach intended behavior, meaningful assertions agree
   with independently reviewed production source/specification, stable replay
   succeeds, and fault detection is measured where an eligible pool exists.
3. **Comparison with the paper:** matched module coverage under explicitly stated
   configurations, followed by broader project-level evidence. Small-screen
   coverage and suite pass alone cannot establish this conclusion.

The paper reports default aggregate line/branch coverage of 83.0%/70.8% on
183 modules; its DeepSeek variant reaches 85.1%/74.2%. It uses three generation
rounds. These are reference targets, not an aggregate baseline for our two-module
one-round screen. Source: [paper v2, evaluation](https://arxiv.org/html/2503.14000v2#S4).

## Current decision and alternatives

| Choice | Evidence/rationale | Cost or risk | Decision rule |
|---|---|---|---|
| Continue the current 14B small screen | Real two-T4 memory calibration passed; cold initialization exhausted the earlier budget | Generation/repair can still time out or produce invalid oracles | Finish the already launched fixed cohort; preserve every outcome |
| Reuse exact greedy initialization | Prior raw outputs, model/runtime/cache keys and source were checked; removes repeated initialization inference | Warm latency excludes historical cold cost; summaries may be wrong/truncated | Import initialization only; record origin and both cold/warm costs |
| Repeat stress/install/CPU fixtures now | Those exact preparation/calibration conditions already passed and were rechecked | Wastes the small-screen budget without measuring generation | Repeat only when a relevant environment, runtime, model or budget changes |
| Switch immediately to 7B | No matched 7B evidence exists yet | Adds a model variable and can sacrifice quality while current evidence is incomplete | Defer until the real 14B bottleneck and quality are measured |
| Launch a large run now | No completed real small measurement yet | Replicates unknown defects and consumes GPU time | Block until the small evidence is reviewed |

The existing 12-module-trial stage is a larger **pilot**, not the 183-module
benchmark. Current production frame: three modules in two projects. A full-paper
comparison additionally requires the complete pinned frame and verified Pyn
project provenance; do not silently replace this requirement with easy modules.

## Gates and stopping decisions

1. **Complete the current small screen.** Two genty modules, two arms, seed42,
   one round, 4096/512 tokens, the same 14B NF4 model, one shared 3600-second
   small-only budget. Never extend its clock or edit its source after outcomes.
2. **Audit before spending another GPU block.** Verify all four planned rows,
   actual worker exit codes, every generation error, candidate retention and
   assertion edits, source hashes, replay, coverage denominators and mutant
   verdicts. Separate missing measurements from measured zero.
3. **If infrastructure fails, fix that failure first.** Identify a reproducible
   cause and make a new versioned cohort. Use the smallest focused regression
   check and real GPU check needed to confirm the correction. Do not rerun
   favorable seeds or change target membership to improve a score.
4. **If tests are weak despite a healthy runner, target the observed mechanism.**
   Review API misuse, missing dependencies, truncation and assertion semantics.
   Any prompt/repair change gets a fresh plan and a matched control. Do not
   hardcode target-specific expected values or feed mutant verdicts to generation.
5. **Choose the next model using quality and cost together.** Measure wall time
   by stage, fresh model calls/tokens, peak VRAM, time to valid measured tests,
   coverage and fault detection. If testing 7B, freeze a separate model revision,
   recalibrate its actual memory configuration and compare against its own matched
   upstream baseline before attributing differences to the method.
6. **Expand in bounded batches after gates pass.** First another locked project
   and multi-round behavior, then a locked multi-project pilot. Forecast the next
   batch from observed project-level costs and the remaining Kaggle budget;
   avoid extrapolating one easy function. Preserve failed projects and partial
   evidence. Validate the complete benchmark's provenance before a full campaign.

## Engineering improvement candidates, not changes to the running study

Prior source/outputs suggest two mechanisms worth investigating if confirmed by
the completed retry: unstructured class context permits property/method misuse;
an instruction to preserve every assertion can obstruct legitimate correction
of an initially incorrect oracle. Generic descriptor inventories and a review
path for oracle corrections are candidates. A static property-call check can
identify some API errors; it cannot certify ordering expectations or semantics.

Checkpointing completed module evidence before final project scoring may reduce
lost measurements on timeout. It requires orchestration tests and explicit
partial-result labels; partial generation must never be reported as a completed
trial. These choices should follow the current run audit rather than be mixed
into its treatment while it is executing.

No strategy guarantees beating the paper. A negative result, a narrower result,
or a resource limit must remain visible and determine the next technical action.

## Resource decisions tied to observations

The current 14B transport decodes roughly 7–11 tokens/second in observed calls;
large suites at a 512-token cap can truncate. Increasing the cap alone may
reduce truncation but increases worst-case latency and requires a new real
memory calibration. Lowering the model size changes quality and runtime at
once. A shared concise-output contract is therefore the first candidate to
prepare offline: it addresses the observed failure without changing weights,
context cap or hardware. It must still pass a new real smoke before adoption.

The prior 39-minute initialization cost is another separate bottleneck. Warm
cache reuse suits unchanged-source iterations, but it does not solve cold-start
latency for a new project. Replacing model summaries with static facts would be
a distinct algorithmic variant requiring its own control and held-out
evaluation, not an unreported shortcut to the original pipeline.
