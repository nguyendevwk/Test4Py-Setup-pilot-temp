"""Internal checks on real pinned PyCG. This module never supplies model context."""
import json
from pathlib import Path
import sys

from pilot.common import BASE, PYCG, checked, write_json
from pilot.scoring import score
from pilot.setup import extract, probe_one, select

# Handwritten oracle is confined to validation, never used as generated output.
ORACLE = '''import os
from pycg.machinery.imports import ImportManager, get_custom_loader

def test_new_destination():
    manager = ImportManager()
    manager.set_current_mod("pkg.main", "main.py")
    manager.create_node("pkg.main")
    get_custom_loader(manager)("pkg.dep", "new.py")
    assert manager.get_filepath("pkg.dep") == os.path.abspath("new.py")

def test_existing_destination():
    manager = ImportManager()
    manager.set_current_mod("pkg.main", "main.py")
    manager.create_node("pkg.main")
    manager.create_node("pkg.dep")
    manager.set_filepath("pkg.dep", "old.py")
    get_custom_loader(manager)("pkg.dep", "new.py")
    assert manager.get_filepath("pkg.dep") == os.path.abspath("old.py")
'''


def main():
    root = Path(sys.argv[1]).resolve()
    work = root.parent
    actual = checked(['git', '-C', root, 'rev-parse', 'HEAD'])
    if actual != PYCG:
        raise RuntimeError('Validation requires pinned real PyCG')
    config = json.loads((BASE / 'pilot.json').read_text())
    extraction = extract(root)
    write_json(work / 'candidates.json', extraction)
    assert extraction['candidate_hash'] == extract(root)['candidate_hash']
    _, selection = select(root, extraction, 'verified', work, config)
    assert selection['complete'], 'Both scenarios must find a valid setup within budget'
    initial = [c for c in extraction['candidates'] if c['id'].endswith(':0')]
    assert all(not probe_one(root, c, config['probe_timeout'])['accepted'] for c in initial)
    test_dir = root / 'Test4DT_tests'
    test_dir.mkdir()
    (test_dir / 'test_internal_oracle.py').write_text(ORACLE)
    result = score(root, work, config)
    assert result['passed'] == 2, result
    assert result['mutation_score'] == 1.0, result
    write_json(work / 'validation.json', dict(status='passed', commit=actual,
        note='Internal handwritten oracle, not model-generated test quality', selection=selection, score=result))
    print('Pinned PyCG: both states, fresh-object probes and two-mutant scorer passed')


if __name__ == '__main__':
    main()
