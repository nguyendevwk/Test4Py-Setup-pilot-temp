"""One fresh-process probe. Observations are private scoring artifacts."""
import json
import os
from pathlib import Path
import sys


def evaluate(root, candidate):
    sys.path.insert(0, str(Path(root).resolve()))
    from pycg.machinery.imports import ImportManager, get_custom_loader
    scope = {'ImportManager': ImportManager}
    try:
        exec(candidate['code'], scope)
        manager = scope['manager']
        existing = candidate['scenario'] == 'existing_target'
        if manager.current_module != 'pkg.main' or not manager.get_node('pkg.main'):
            raise ValueError('source module has no current graph node')
        if bool(manager.get_node('pkg.dep')) != existing:
            raise ValueError('destination presence does not match scenario')
        if existing and manager.get_filepath('pkg.dep') != os.path.abspath('old.py'):
            raise ValueError('destination does not have old filepath')
        get_custom_loader(manager)('pkg.dep', 'new.py')
        return dict(accepted=True, reason='preconditions and invocation succeeded',
                    filepath=manager.get_filepath('pkg.dep'))
    except Exception as exc:
        return dict(accepted=False, reason=f'{type(exc).__name__}: {exc}')


if __name__ == '__main__':
    print(json.dumps(evaluate(sys.argv[1], json.loads(sys.argv[2]))))
