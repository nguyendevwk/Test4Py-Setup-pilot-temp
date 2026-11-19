"""Behavioral checks with hand-computable synthetic studies; no API access."""
import copy
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path

import numpy as np
import pytest

SPEC = importlib.util.spec_from_file_location('full_scope_statistics', Path(__file__).resolve().parents[1] / 'scripts/analyze_groq_full_scope.py')
stats = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(stats)


def study():
    # A small project favors context; a three-target project favors source.
    targets = [dict(id=str(i), project='small' if i == 0 else 'large', module=f'm{i}') for i in range(4)]
    manifest = dict(targets=targets, seed_values=[71, 72], arms=list(stats.ARMS), planned=24,
                    provenance={'scope': 'synthetic fixture only'})
    rows = []
    for t, seed, arm in itertools.product(targets, [71, 72], stats.ARMS):
        accepted = (t['project'] == 'small' and arm == 'context_setup') or (t['project'] == 'large' and arm == 'source')
        rows.append(dict(target_id=t['id'], project=t['project'], module=t['module'], seed=seed,
                         arm=arm, accepted=accepted, status='completed' if accepted else 'test_failure', line_pct=80 if accepted else 99))
    return manifest, dict(rows=rows, planned=24, completed=24)


@pytest.mark.parametrize('corruption', ['missing', 'duplicate', 'replacement', 'module', 'project',
                                        'infrastructure', 'incomplete', 'planned', 'boolean', 'accepted_failure', 'coverage'])
def test_completeness_and_integrity_reject_before_inference(corruption):
    m, s = study()
    if corruption == 'missing':
        s['rows'].pop()
    elif corruption == 'duplicate':
        s['rows'].append(copy.deepcopy(s['rows'][0]))
    elif corruption == 'replacement':
        s['rows'][-1] = copy.deepcopy(s['rows'][0])  # same count is insufficient
    elif corruption in ('module', 'project'):
        s['rows'][0][corruption] = 'wrong'
    elif corruption == 'infrastructure':
        s['rows'][0]['status'] = 'api_error'
    elif corruption == 'incomplete':
        s['completed'] -= 1
    elif corruption == 'planned':
        m['planned'] -= 1
    elif corruption == 'boolean':
        s['rows'][0]['accepted'] = 1
    elif corruption == 'accepted_failure':
        s['rows'][0].update(accepted=True, status='replay_failure')
    else:
        s['rows'][2]['line_pct'] = float('nan')
    with pytest.raises(ValueError):
        stats.analyze(m, s)


def test_all_specified_model_terminal_failures_are_denominator_members():
    m, s = study()
    failures = sorted(stats.TERMINAL - {'completed'})
    for row, status in zip((r for r in s['rows'] if not r['accepted']), failures):
        row.update(status=status, line_pct=None)
    out = stats.analyze(m, s)
    assert out['completed'] == 24
    assert sum(a['denominator'] for a in out['arms'].values()) == 24


def test_equal_projects_not_pooled_attempts_and_failure_coverage_is_zero():
    out = stats.analyze(*study())
    c = out['contrasts']['context_setup-source']
    assert c['difference'] == 0  # (+1 - 1)/2; pooled difference would be -0.5
    assert c['project_differences'] == {'large': -1, 'small': 1}
    context = out['arms']['context_setup']
    assert context['equal_project_acceptance_rate'] == .5
    assert context['successes'] == 2 and context['denominator'] == 8
    assert context['equal_project_penalized_module_line_pct'] == 40
    assert context['pooled_penalized_module_line_pct_descriptive'] == 20
    assert out['per_project']['large']['arms']['source']['successes'] == 6
    assert out['per_project']['small']['arms']['source']['denominator'] == 2
    assert 'holm_adjusted_p' not in c
    assert stats.analyze(*study()) == out


@pytest.mark.parametrize('effects', [[1, 1, 1], [0, 0], [.25, -.5, 0, 1], [.1, .2, -.3]])
def test_exact_signflip_matches_independent_bruteforce_with_ties(effects):
    observed = abs(sum(effects))
    values = [abs(sum(s * x for s, x in zip(signs, effects)))
              for signs in itertools.product([-1, 1], repeat=len(effects))]
    expected = sum(v >= observed - 1e-12 for v in values) / len(values)
    assert stats.exact_signflip(effects, chunk_size=3) == expected


def test_exact_twenty_one_projects_and_zero_effects():
    assert stats.exact_signflip(np.ones(21)) == 2 / 2**21
    assert stats.exact_signflip(np.zeros(21)) == 1


@pytest.mark.parametrize('raw,expected', [([.03, .04], [.06, .06]), ([.04, .01], [.04, .02]),
                                         ([.8, .9], [1., 1.]), ([.02, .02], [.04, .04])])
def test_holm_two_secondary_family_order_monotonicity_and_cap(raw, expected):
    assert stats.holm(raw) == pytest.approx(expected)


def test_cli_final_artifacts_hashes_and_refusal_does_not_overwrite(tmp_path):
    m, s = study()
    for name, data in [('manifest.json', m), ('summary.json', s)]:
        (tmp_path / name).write_text(json.dumps(data))
    stats.main(['--study', str(tmp_path)])
    out = json.loads((tmp_path / 'statistics.json').read_text())
    assert (tmp_path / 'stats.json').read_bytes() == (tmp_path / 'statistics.json').read_bytes()
    for name in ['manifest.json', 'summary.json']:
        assert out['input_sha256'][name] == hashlib.sha256((tmp_path / name).read_bytes()).hexdigest()
    assert 'conditional' in (tmp_path / 'STATISTICS.md').read_text()
    previous = {name: (tmp_path / name).read_bytes() for name in ['stats.json', 'statistics.json', 'STATISTICS.md']}
    s['rows'].pop()
    (tmp_path / 'summary.json').write_text(json.dumps(s))
    with pytest.raises(SystemExit) as exc:
        stats.main(['--study', str(tmp_path)])
    assert exc.value.code == 2
    assert all((tmp_path / name).read_bytes() == content for name, content in previous.items())
    for name in previous:
        (tmp_path / name).unlink()
    with pytest.raises(SystemExit):
        stats.main(['--study', str(tmp_path)])
    assert all(not (tmp_path / name).exists() for name in previous)
