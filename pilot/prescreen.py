"""Small integration-screen statistics. Samples are generations of ONE target."""
import math
import random


def sample_ids(total, fraction, limit, seed):
    if total < 1 or not 0 < fraction <= 1 or limit is not None and limit < 1:
        raise ValueError('population/limit must be positive and fraction in (0,1]')
    count = min(total, limit if limit is not None else math.ceil(total * fraction))
    return sorted(random.Random(seed).sample(range(total), count))


def summarize(rows, planned):
    finished = [r for r in rows if r.get('status') in {'evaluated','generation_error','extraction_error','environment_error'}]
    generated = [r for r in finished if r.get('status')=='evaluated']
    def rate(n, d): return n/d if d else None
    passed = sum(r.get('passed',0)>0 for r in finished)
    stable = [r for r in finished if r.get('stable') is not None]
    mutants = [m for r in finished for m in r.get('mutants',[])]
    resolved = [m for m in mutants if m.get('verdict') in {'killed','survived'}]
    return dict(planned_candidates=planned, finished_candidates=len(finished),
        remaining_candidates=max(0,planned-len(finished)), evaluated_candidates=len(generated),
        ast_valid_candidates=sum(r.get('ast_parse') is True for r in finished),
        original_passing_candidates=passed, original_passing_candidate_rate=rate(passed,len(finished)),
        original_passing_tests=sum(r.get('passed',0) for r in finished),
        stable_candidates=sum(r.get('stable') is True for r in stable), stability_audited=len(stable),
        mutant_runs=len(mutants), resolved_mutant_runs=len(resolved),
        killed_mutant_runs=sum(m.get('verdict')=='killed' for m in mutants),
        mutation_score=rate(sum(m.get('verdict')=='killed' for m in mutants),len(mutants))
            if mutants and len(resolved)==len(mutants) else None,
        input_tokens=sum(r.get('input_tokens',0) for r in finished),
        output_tokens=sum(r.get('output_tokens',0) for r in finished),
        sample_seconds=sum(r.get('seconds',0) for r in finished),
        semantic_assertion_accuracy=None,
        quality_gate='review_required: passing tests and coverage do not establish oracle correctness',
        independent_targets=1, inference='development integration screen; not full Test4Py, not 100 independent targets')
