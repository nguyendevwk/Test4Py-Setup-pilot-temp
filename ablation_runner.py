"""Ablation Study Runner and Result Aggregator for Test4Py Council Paper."""
import argparse
import json
from pathlib import Path

from pilot.common import BASE, reserve_output, write_json
from council.runner import run_council_pipeline

VARIANTS = {
    "full_14b": {
        "name": "Full Council (Proposed)",
        "coder_model": "Qwen/Qwen2.5-Coder-14B-Instruct",
        "critic_model": "Qwen/Qwen3-4B-Instruct-2507",
        "mode": "council",
        "no_repair": False,
        "desc": "Full Council with Fixture Architect, Coder 14B, and Critic Repair",
    },
    "no_fixture_14b": {
        "name": "w/o Fixture Architect",
        "coder_model": "Qwen/Qwen2.5-Coder-14B-Instruct",
        "critic_model": "Qwen/Qwen3-4B-Instruct-2507",
        "mode": "baseline",
        "no_repair": False,
        "desc": "Ablation: Removes Verified Setup Context (raw source only)",
    },
    "no_critic_14b": {
        "name": "w/o Critic Self-Repair",
        "coder_model": "Qwen/Qwen2.5-Coder-14B-Instruct",
        "critic_model": "Qwen/Qwen3-4B-Instruct-2507",
        "mode": "council",
        "no_repair": True,
        "desc": "Ablation: Disables Critic repair loop (single-shot Coder)",
    },
    "scale_7b": {
        "name": "Coder 7B Scale",
        "coder_model": "Qwen/Qwen2.5-Coder-7B-Instruct",
        "critic_model": "Qwen/Qwen3-4B-Instruct-2507",
        "mode": "council",
        "no_repair": False,
        "desc": "Model Scale: Coder 7B with Critic Repair",
    },
    "scale_3b": {
        "name": "Coder 3B Scale",
        "coder_model": "Qwen/Qwen2.5-Coder-3B-Instruct",
        "critic_model": "Qwen/Qwen3-4B-Instruct-2507",
        "mode": "council",
        "no_repair": False,
        "desc": "Model Scale: Coder 3B with Critic Repair",
    },
}

for _key, _mode in (('extracted_14b', 'extracted'), ('ranked_14b', 'ranked'), ('caller_14b', 'caller')):
    VARIANTS[_key] = dict(VARIANTS['full_14b'], name=_mode+' setup control', mode=_mode,
                          desc='Same coder and repair; setup selection without runtime verification')
VARIANTS['self_repair_14b'] = dict(VARIANTS['full_14b'], name='Coder self-repair',
    repair_with='coder', desc='Same one-repair budget using coder instead of a second model')


def compile_ablation_reports(runs_dir: Path) -> str:
    """Separate cohorts, reject legacy/mock records, expose conditional denominators."""
    from collections import defaultdict
    groups = defaultdict(list)
    warnings = []
    for path in sorted(runs_dir.rglob("summary.json")):
        try:
            data = json.loads(path.read_text())
            if not isinstance(data, dict):
                raise ValueError("summary must be an object")
            if data.get("schema_version") != 2:
                raise ValueError("legacy/unsupported schema; rerun or audit raw artifacts")
            if data.get("mock") is not False or data.get("run_kind") != "real":
                raise ValueError("mock/non-real output excluded from efficacy table")
            if not data.get("cohort") or not isinstance(data.get("results"), list):
                raise ValueError("missing cohort or results")
            if data.get("planned_samples", 0) < 1:
                raise ValueError("missing planned denominator")
            data["_path"] = str(path.relative_to(runs_dir))
            groups[data["cohort"]].append(data)
        except (ValueError, TypeError, OSError) as exc:
            warnings.append(f"{path.relative_to(runs_dir)}: {exc}")
    lines = ["# Council development case study comparison", "",
             "One target; repeated greedy generations are not independent targets.",
             "Baseline = Council without setup, not upstream Test4Py.",
             "Means are conditional on complete scoring; n/planned is shown for each metric.",
             "No scores are imputed for infrastructure failures or missing tests.",
             "Changed prompts/scorers/budgets form separate cohorts. Model scale is a separate factor.", ""]
    for cohort, summaries in groups.items():
        lines += [f"## Cohort `{cohort}`", "",
            "| Run | Coder @ revision | Mode / Repair | Run status | Finished / Planned | First-pass / Planned | All-pass / Planned | Module branch mean (n/planned) | Target+nested branch mean (n/planned) | Two-mutant mean (n/planned) | Missing reasons |",
            "|---|---|---|---|---:|---:|---:|---:|---:|---:|---|"]
        for data in summaries:
            rows = data['results']; planned = data['planned_samples']
            complete = [r for r in rows if r.get('scoring_complete') is True]
            pools = {r.get('mutant_pool_hash') for r in complete}
            if len(pools) > 1 or None in pools:
                warnings.append(data['_path']+': inconsistent/missing mutant pool; mutation mean withheld')
            def metric(key, decimals):
                values = [r[key] for r in complete if r.get(key) is not None]
                if key == 'mutation_score' and (len(pools) > 1 or None in pools):
                    values = []
                return (f"{sum(values)/len(values):.{decimals}f}" if values else "NA") + f" ({len(values)}/{planned})"
            first = sum(r.get('first_pass') is True for r in rows)
            passed = sum(r.get('suite_all_pass') is True for r in rows)
            from collections import Counter
            reasons = Counter(r.get('score_status', r.get('status', 'unknown')) for r in rows
                              if r.get('scoring_complete') is not True)
            if len(rows) < planned:
                reasons['not_finished'] += planned-len(rows)
            models = data.get('engine', {}).get('models', {})
            revision = models.get('coder', {}).get('revision', 'MISSING')
            critic_revision = models.get('critic', {}).get('revision')
            repair = 'disabled' if data.get('no_repair') else data.get('repair_with', 'critic')
            if repair == 'critic':
                repair += ' '+data.get('critic_model', '?')+'@'+str(critic_revision)
            lines.append(f"| `{data['_path']}` | {data.get('coder_model')} @ {revision} | {data.get('mode')} / {repair} | {data.get('status')} | {len(rows)}/{planned} | {first}/{planned} | {passed}/{planned} | {metric('branch_pct', 2)} | {metric('target_branch_pct', 2)} | {metric('mutation_score', 2)} | {dict(reasons)} |")
    if not groups:
        lines += ['No compatible real-run summaries found.', '']
    lines += ['', '## Excluded records and warnings', '']
    lines += ['- '+warning for warning in warnings] or ['- None.']
    content = "\n".join(lines)+"\n"
    runs_dir.mkdir(parents=True, exist_ok=True)
    (runs_dir/'ablation_comparison.md').write_text(content)
    return content


def run_single_variant(variant_key: str, samples: int, base_output: Path, mock: bool = False,
                       max_new_tokens=2048, seed=42, revisions=None):
    cfg = VARIANTS[variant_key]
    out_dir = base_output / f"ablation_{variant_key}"
    print("\n" + "=" * 70)
    print(f"🔬 RUNNING ABLATION VARIANT: {cfg['name']}")
    print(f"  • Description: {cfg['desc']}")
    print(f"  • Coder: {cfg['coder_model']}")
    print(f"  • Critic: {cfg['critic_model']}")
    print(f"  • Mode: {cfg['mode']} | No-Repair: {cfg['no_repair']}")
    print(f"  • Output: {out_dir}")
    print("=" * 70, flush=True)

    class Args:
        pass

    args = Args()
    args.samples = samples
    args.mode = cfg["mode"]
    args.fast = False
    args.coder_model = cfg["coder_model"]
    args.critic_model = cfg["critic_model"]
    args.no_repair = cfg["no_repair"]
    args.max_new_tokens = max_new_tokens
    args.seed = seed
    args.repair_with = cfg.get('repair_with', 'critic')
    revisions = revisions if revisions is not None else {}
    args.coder_revision = revisions.get(args.coder_model, 'main')
    args.critic_revision = revisions.get(args.critic_model, 'main')
    args.load_in_4bit = True
    args.mock = mock
    args.output = out_dir

    summary = run_council_pipeline(args)
    for record in summary.get('engine', {}).get('models', {}).values():
        revisions[record['name']] = record['revision']
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variant", choices=list(VARIANTS.keys()) + ["all"], default="full_14b",
                        help="Specific ablation variant to run")
    parser.add_argument("--samples", type=int, default=2, help="Number of samples per variant")
    parser.add_argument("--output", type=Path, default=BASE / "runs" / "ablation_study")
    parser.add_argument("--max-new-tokens", type=int, default=2048)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--mock", action="store_true", help="Run with mock LLM for offline validation")
    parser.add_argument("--compile", action="store_true", help="Compile existing summary files into Markdown table")
    args = parser.parse_args()

    if args.compile:
        if not args.output.is_dir():
            parser.error("output directory does not exist; refusing to scan an unrelated directory")
        report = compile_ablation_reports(args.output)
        print(report)
        return

    if args.samples < 1 or args.max_new_tokens < 1:
        parser.error('positive samples and max-new-tokens required')
    import random
    variants = list(VARIANTS) if args.variant == 'all' else [args.variant]
    random.Random(args.seed).shuffle(variants)
    batch = reserve_output(args.output)
    write_json(batch/'batch_manifest.json', dict(order=variants, seed=args.seed,
        samples=args.samples, max_new_tokens=args.max_new_tokens, mock=args.mock,
        inference='one-target development case study; no statistical generalization'))
    revisions = {}
    failed = False
    for key in variants:
        result = run_single_variant(key, args.samples, batch, args.mock,
                                    args.max_new_tokens, args.seed, revisions)
        failed = failed or result['status'] in {'failed', 'complete_with_errors'}
    print(compile_ablation_reports(batch))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
