"""Bounded production-source retrieval and callable invocation witnesses.

No tests, benchmark outcomes, mutant observations or return values enter context.
Rules depend on Python AST/signatures, not project/symbol-name allowlists.
"""
import ast
from collections import deque
from pathlib import Path
import json
import sys

from pilot.common import command
from pilot.multitarget import checkout_env


def dependency_context(root, relative_file, symbol, max_chars=10000, max_nodes=10):
    root = Path(root).resolve()
    start = (root/relative_file).resolve()
    if not start.is_relative_to(root):
        raise ValueError('Source outside checkout')
    cache = {}
    def module_file(parts):
        for prefix in (root, root/'src'):
            for p in (prefix.joinpath(*parts).with_suffix('.py'), prefix.joinpath(*parts)/'__init__.py'):
                if (p.is_file() and p.resolve().is_relative_to(root)
                    and not any(part in ('test', 'tests', '__pycache__') for part in p.relative_to(root).parts)
                    and not p.name.startswith('test_')):
                    return p.resolve()
        return None
    def index(path):
        if path in cache:
            return cache[path]
        text = path.read_text()
        tree = ast.parse(text)
        definitions, imports = {}, {}
        rel = path.relative_to(root)
        parts = list(rel.with_suffix('').parts)
        if parts[0] == 'src':
            parts = parts[1:]
        package = parts[:-1]
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                definitions[node.name] = node
            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                names = node.targets if isinstance(node, ast.Assign) else [node.target]
                for name in names:
                    if isinstance(name, ast.Name):
                        definitions[name.id] = node
            elif isinstance(node, ast.ImportFrom):
                prefix = package[:len(package)-node.level+1] if node.level else []
                prefix += node.module.split('.') if node.module else []
                target = module_file(prefix)
                for alias in node.names:
                    if target and alias.name != '*':
                        imports[alias.asname or alias.name] = (target, alias.name)
        cache[path] = text, definitions, imports
        return cache[path]
    def references(node):
        # Return annotations first: useful result-object properties often live there.
        result = []
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.returns:
            result.extend(n.id for n in ast.walk(node.returns) if isinstance(n, ast.Name))
        result.extend(n.id for n in ast.walk(node) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load))
        return list(dict.fromkeys(result))
    text, defs, _ = index(start)
    container = symbol.split('.')[0]
    if container not in defs:
        raise ValueError('Dependency retrieval target missing')
    queue = deque([(start, name, 1) for name in references(defs[container])])
    seen, snippets, omitted = {(start, container)}, [], []
    if '.' in symbol:
        node = defs[container]
        excerpt = ast.get_source_segment(text, node) or ''
        if len(excerpt) <= max_chars:
            snippets.append(dict(file=str(start.relative_to(root)), line=node.lineno, symbol=container, source=excerpt))
        else:
            omitted.append(container)
    used = sum(len(n['source']) for n in snippets)
    while queue:
        path, name, depth = queue.popleft()
        if (path, name) in seen:
            continue
        seen.add((path, name))
        text, defs, imports = index(path)
        if name in imports:
            dep_path, dep_name = imports[name]
            if (dep_path, dep_name) not in seen:
                queue.appendleft((dep_path, dep_name, depth))
        if name not in defs:
            continue
        node = defs[name]
        snippet = ast.get_source_segment(text, node) or ''
        label = f'{path.relative_to(root)}:{node.lineno} {name}'
        if len(snippets) >= max_nodes or used+len(snippet) > max_chars:
            omitted.append(label)
            continue
        snippets.append(dict(file=str(path.relative_to(root)), line=node.lineno, symbol=name, source=snippet))
        used += len(snippet)
        if depth < 2:
            queue.extend((path, ref, depth+1) for ref in references(node))
    return dict(policy='production-dependencies-v1', max_chars=max_chars, max_nodes=max_nodes,
                chars=used, snippets=snippets, omitted=omitted,
                scope='static source excerpts only; no inferred expected values')


def verify_target_invocation(setup, root, module, symbol, timeout=8):
    """Witness target entry with setup values; no oracle or output-value assertions.

    Class scope is constructor only. Function candidates use existing setup values,
    prefer matching names/annotations and use one deterministic binding. No retries via the LLM.
    """
    script = '''import importlib, inspect, itertools, json, sys
SETUP = SETUP_VALUE
MODULE = MODULE_VALUE
SYMBOL = SYMBOL_VALUE
obj = importlib.import_module(MODULE)
for part in SYMBOL.split('.'):
    obj = getattr(obj, part)
scope = {}
seen = []
code = getattr(obj.__init__ if inspect.isclass(obj) else obj, '__code__', None)
def trace(frame, event, arg):
    if event == 'call' and code is not None and frame.f_code is code:
        seen.append(True)
sys.setprofile(trace)
try:
    exec(SETUP, scope)
    if inspect.isclass(obj):
        ok = bool(seen) and any(isinstance(v, obj) for k,v in scope.items() if not k.startswith('__'))
        result = dict(accepted=ok, invocation=None, scope='constructor entry only; no method-state guarantee')
    else:
        signature = inspect.signature(obj)
        required = [p for p in signature.parameters.values() if p.default is inspect.Parameter.empty
                    and p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD, p.KEYWORD_ONLY)]
        values = [(k,v) for k,v in scope.items() if not k.startswith('_') and not inspect.ismodule(v) and not callable(v)]
        # Prefer actual parameter-name matches, then setup literal values in source order.
        pools = []
        for p in required:
            ordered = sorted(values, key=lambda kv: kv[0] != p.name)
            annotation = p.annotation
            if annotation in (str, int, float, bool, list, dict, tuple):
                ordered = sorted(ordered, key=lambda kv: not isinstance(kv[1], annotation))
            pools.append(ordered[:3])
        result = dict(accepted=False, invocation=None, scope='target function entry and normal completion')
        for attempt, selected in enumerate(itertools.product(*pools)):
            if attempt >= 1:
                break
            args, kwargs, expressions = [], {}, []
            for p, (name,value) in zip(required, selected):
                if p.kind == p.POSITIONAL_ONLY:
                    args.append(value); expressions.append(name)
                else:
                    kwargs[p.name] = value; expressions.append(p.name+'='+name)
            seen.clear()
            try:
                obj(*args, **kwargs)
                if seen:
                    result.update(accepted=True, invocation='import importlib\\n_target = importlib.import_module('+repr(MODULE)+')'+''.join('.'+part for part in SYMBOL.split('.'))+'\\n_target('+', '.join(expressions)+')')
                    break
            except Exception:
                pass
finally:
    sys.setprofile(None)
print(json.dumps(result))
'''.replace('SETUP_VALUE', repr(setup)).replace('MODULE_VALUE', repr(module)).replace('SYMBOL_VALUE', repr(symbol))
    proc = command([sys.executable, '-c', script], cwd=root, env=checkout_env(root), timeout=timeout)
    try:
        result = json.loads((proc.get('stdout') or '').splitlines()[-1])
    except (ValueError, IndexError):
        result = dict(accepted=False, scope='invocation unavailable')
    result['accepted'] = bool(result['accepted'] and not proc['timeout'] and proc['returncode'] == 0)
    result['process'] = proc
    return result


def load_target_spec(path):
    """External locked benchmark frame; no target selection based on run outcomes."""
    import re
    payload = json.loads(Path(path).read_text())
    targets = payload['targets'] if isinstance(payload, dict) else payload
    if not isinstance(targets, list) or not targets:
        raise ValueError('Target specification must contain a nonempty targets list')
    seen = set()
    for target in targets:
        required = ('id', 'project', 'repo_url', 'commit', 'module', 'file', 'symbol')
        if not isinstance(target, dict) or any(not isinstance(target.get(k), str) or not target[k] for k in required):
            raise ValueError('Target specification missing required string fields')
        if target['id'] in seen:
            raise ValueError('Duplicate target id')
        seen.add(target['id'])
        for key in ('id', 'project'):
            if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', target[key]) or '..' in target[key]:
                raise ValueError('Unsafe target id/project')
        relative = Path(target['file'])
        if relative.is_absolute() or '..' in relative.parts or relative.suffix != '.py':
            raise ValueError('Invalid production source file')
        if any(p in ('test', 'tests', '__pycache__') for p in relative.parts) or relative.name.startswith('test_'):
            raise ValueError('Test source cannot be a benchmark production target')
        if not re.fullmatch(r'[0-9a-fA-F]{40}', target['commit']):
            raise ValueError('External benchmark commits must be immutable 40-character SHAs')
        if not all(p.isidentifier() for p in target['module'].split('.')) or not all(p.isidentifier() for p in target['symbol'].split('.')):
            raise ValueError('Invalid module/symbol')
    return targets
