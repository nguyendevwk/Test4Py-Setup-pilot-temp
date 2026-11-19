"""Small deterministic fault pool for module-level paired pilots.

Not a comprehensive mutation benchmark. Equivalent mutants are not automatically
identified. Pools are frozen before model execution and never shown to the LLM.
"""
import ast
import copy
import hashlib


def pool(source, limit=4):
    tree = ast.parse(source)
    replacements = {ast.Eq: ast.NotEq, ast.NotEq: ast.Eq, ast.Lt: ast.LtE,
                    ast.LtE: ast.Lt, ast.Gt: ast.GtE, ast.GtE: ast.Gt,
                    ast.Add: ast.Sub, ast.Sub: ast.Add, ast.Mult: ast.Add}
    candidates = []
    def walk(node, owners=(), in_function=False):
        owners = owners+(node.name,) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) else owners
        in_function = in_function or isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        if in_function and isinstance(node, (ast.Compare, ast.BinOp)):
            ops = node.ops if isinstance(node, ast.Compare) else [node.op]
            for i, op in enumerate(ops):
                if type(op) in replacements:
                    candidates.append((node, i, replacements[type(op)], '.'.join(owners), type(op).__name__))
        for child in ast.iter_child_nodes(node):
            walk(child, owners, in_function)
    walk(tree)
    positions = {id(node): index for index,node in enumerate(ast.walk(tree))}
    results = []
    for index, (target, op_index, replacement, owner, old) in enumerate(candidates[:limit]):
        mutant = copy.deepcopy(tree)
        # Nested left-associative expressions can share start coordinates.
        # Deepcopy preserves traversal order, so select the exact original node.
        node = list(ast.walk(mutant))[positions[id(target)]]
        if isinstance(node, ast.Compare):
            node.ops[op_index] = replacement()
        else:
            node.op = replacement()
        ast.fix_missing_locations(mutant)
        text = ast.unparse(mutant)+'\n'
        compile(text, '<mutant>', 'exec')
        results.append(dict(id=f'm{index:03d}', line=target.lineno, owner=owner,
                           operator=old+'->'+replacement.__name__, source=text,
                           sha256=hashlib.sha256(text.encode()).hexdigest()))
    return dict(original_sha256=hashlib.sha256(source.encode()).hexdigest(), mutants=results,
                scope='bounded comparison/arithmetic operators; equivalent mutants not filtered')


def verdict(process, report, eligible):
    if process.get('timeout'):
        return 'timeout_inconclusive'
    tests = {r['nodeid']: r for r in report.get('tests', [])}
    if process.get('returncode') not in (0, 1) or set(tests) != set(eligible):
        return 'execution_inconclusive'
    for t in tests.values():
        if any(t.get(p, {}).get('outcome') != 'passed' for p in ('setup', 'teardown')):
            return 'execution_inconclusive'
        if t.get('call', {}).get('outcome') not in ('passed', 'failed'):
            return 'execution_inconclusive'
        text = str(t.get('call', {}))
        if any(error in text for error in ('ImportError', 'ModuleNotFoundError')):
            return 'execution_inconclusive'
    if any(t['call']['outcome'] == 'failed' for t in tests.values()):
        return 'killed'
    return 'survived' if process['returncode'] == 0 else 'execution_inconclusive'
