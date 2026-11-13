"""PyCG-specific AST extraction. No test source or probe output enters prompts."""
import ast
import itertools
import json
import os
from pathlib import Path
import sys
import time

from pilot.common import BASE, append_json, command, digest, write_json

SCENARIOS = ('new_target', 'existing_target')


def production(path):
    return not any(p in {'tests', 'test', '__pycache__', '.git'} for p in path.parts) and not (
        path.name.startswith('test_') or path.stem.endswith('_test'))


def extract(root):
    started = time.perf_counter()
    root = Path(root)
    evidence = []
    # Pilot rule: recognize calls through self.import_manager. Argument
    # substitution and the operation allowlist below are explicitly PyCG-specific.
    for path in sorted((root / 'pycg').rglob('*.py')):
        relative = path.relative_to(root)
        if not production(relative):
            continue
        source = path.read_text()
        tree = ast.parse(source)
        parents = {child: node for node in ast.walk(tree) for child in ast.iter_child_nodes(node)}
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
                continue
            if ast.unparse(node.func.value) != 'self.import_manager':
                continue
            if node.func.attr not in {'set_current_mod', 'create_node', 'set_filepath'}:
                continue
            owner = node
            while owner in parents and not isinstance(owner, (ast.FunctionDef, ast.AsyncFunctionDef)):
                owner = parents[owner]
            evidence.append(dict(operation=node.func.attr, file=str(relative), line=node.lineno,
                                 end_line=node.end_lineno, call=ast.get_source_segment(source, node),
                                 snippet=ast.get_source_segment(source, owner)))
    operations = {
        'set_current_mod': 'manager.set_current_mod("pkg.main", "main.py")',
        'create_node': 'manager.create_node("pkg.main")',
    }
    required = set(operations)
    if not required.issubset({e['operation'] for e in evidence}):
        raise RuntimeError('Required production caller evidence missing')
    # Deterministic shortest-first search; lexicographic operation order breaks ties.
    # Constructor-only is a real first candidate, not an injected synthetic failure.
    sequences = [()] + [seq for size in (1, 2)
                         for seq in itertools.permutations(sorted(operations), size)]
    candidates = []
    for index, sequence in enumerate(sequences):
        for scenario in SCENARIOS:
            statements = ['from pycg.machinery.imports import ImportManager',
                          'manager = ImportManager()', *(operations[n] for n in sequence)]
            if scenario == 'existing_target':
                statements += ['manager.create_node("pkg.dep")',
                               'manager.set_filepath("pkg.dep", "old.py")']
            candidates.append(dict(id=f'{scenario}:{index}', scenario=scenario,
                                   operations=list(sequence), code='\n'.join(statements),
                                   evidence=[e for e in evidence if e['operation'] in sequence]))
    return dict(candidates=candidates, evidence=evidence,
                candidate_hash=digest(candidates), seconds=time.perf_counter() - started,
                rules='PyCG allowlist; literal argument substitution; constructor then shortest permutations; '
                      'existing destination fixture uses create_node/set_filepath; not general synthesis')


def probe_one(root, candidate, timeout):
    env = dict(os.environ, PYTHONPATH=str(BASE), PYTHONDONTWRITEBYTECODE='1')
    result = command([sys.executable, '-m', 'pilot.probe', str(Path(root).resolve()),
                      json.dumps(candidate)], cwd=root, env=env, timeout=timeout)
    payload = None
    try:
        payload = json.loads(result['stdout'].splitlines()[-1])
    except (ValueError, IndexError):
        pass
    return dict(candidate_id=candidate['id'], scenario=candidate['scenario'],
                accepted=bool(payload and payload.get('accepted') and result['returncode'] == 0),
                reason='timeout' if result['timeout'] else (
                    payload.get('reason') if payload else 'probe process/environment failure'),
                observation=payload, process=result)


def select(root, extraction, mode, work, config):
    started = time.perf_counter()
    work = Path(work)
    selected, probes = {}, []
    if mode == 'verified':
        # Budget counts actual fresh-process probes across both scenarios.
        for candidate in extraction['candidates']:
            if candidate['scenario'] in selected:
                continue
            if len(probes) >= config['max_probes']:
                break
            result = probe_one(root, candidate, config['probe_timeout'])
            probes.append(result)
            append_json(work / 'probes.jsonl', result)
            if result['accepted']:
                selected[candidate['scenario']] = candidate
    elif mode == 'extracted':
        for candidate in extraction['candidates']:
            selected.setdefault(candidate['scenario'], candidate)
    context = ''
    if mode == 'caller':
        # Original product snippets only, no test source and no probe evidence.
        snippets = sorted({f"{e['file']}:{e['line']}\n{e['snippet']}"
                           for e in extraction['evidence']
                           if e['operation'] in {'set_current_mod', 'create_node'}})
        context = 'Production caller context (PyCG):\n' + '\n\n'.join(snippets)
    elif mode in {'extracted', 'verified'}:
        context = 'Candidate setup examples (derive assertions from production code):\n' + '\n\n'.join(
            f"{name}:\n```python\n{value['code']}\n```" for name, value in selected.items())
    selection = dict(mode=mode, selected={k: v['id'] for k, v in selected.items()},
                     candidate_hash=extraction['candidate_hash'], probes=len(probes),
                     seconds=time.perf_counter() - started,
                     complete=len(selected) == 2 if mode in {'extracted', 'verified'} else True,
                     prompt_context=context)
    write_json(work / 'selection.json', selection)
    return context, selection
