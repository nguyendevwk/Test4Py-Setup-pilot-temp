"""Compact, source-only API shape evidence. Never executes a project or oracle."""
import ast
import hashlib
import json
from pathlib import Path

POLICY = 'api-contract-v1'
OPERATIONS = frozenset({'generate_test_case_normal', 'generate_test_case_easy',
    'generate_test_case_evol', 'repair_syntax_error', 'repair_assert_error'})
COMMON_INSTRUCTION = (
    'Return a complete concise Python pytest file in one code block, within the output budget. '
    'Focus on the current target API rather than an entire unrelated suite; multiple tests are allowed '
    'but keep the file focused and under 35 lines to avoid truncation. '
    'Call the real production implementation; never redefine or mock the target. '
    'Always explicitly import pytest and all required dependencies at the top. '
    'Treat generated summaries/examples as unverified. Derive assertions from production source/specification, '
    'not by copying observed outputs. Keep existing tests and checks when repairing.'
)


def candidate_accepted(upstream_accepted, audit, arm, policy=None):
    if policy not in (None, 'upstream', 'preserve-assertions-v1'):
        raise ValueError('Unknown common acceptance policy')
    strict = policy == 'preserve-assertions-v1' or policy is None and arm == 'improved'
    return bool(upstream_accepted and (not strict or audit['accepted'] and not audit.get('review_required', False)))


def _signature(node):
    result = '(' + ast.unparse(node.args) + ')'
    if node.returns is not None:
        result += ' -> ' + ast.unparse(node.returns)
    return result


def _bindings(node):
    """Bindings of one lexical function, excluding bodies of inner scopes."""
    names = {a.arg for a in (*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs)}
    names.update(a.arg for a in (node.args.vararg, node.args.kwarg) if a is not None)
    class Bindings(ast.NodeVisitor):
        def visit_Name(self, item):
            if isinstance(item.ctx, ast.Store): names.add(item.id)
        def visit_FunctionDef(self, item): names.add(item.name)
        visit_AsyncFunctionDef = visit_FunctionDef
        def visit_ClassDef(self, item): names.add(item.name)
        def visit_Import(self, item):
            names.update(a.asname or a.name.split('.')[0] for a in item.names)
        def visit_ImportFrom(self, item):
            names.update(a.asname or a.name for a in item.names)
    visitor = Bindings()
    for item in node.body: visitor.visit(item)
    return names


def build_api_contract(root, relative_file, symbol, max_chars=2500):
    root = Path(root).resolve()
    path = (root / relative_file).resolve()
    if (not path.is_relative_to(root) or path.suffix != '.py'
            or any(p in ('test', 'tests', '__pycache__') for p in path.relative_to(root).parts)
            or path.name.startswith('test_')):
        raise ValueError('API evidence requires production source inside the checkout')
    if max_chars < 256:
        raise ValueError('API evidence budget too small')
    source = path.read_text()
    tree = ast.parse(source)
    functions, classes = [], []
    def walk(body, ancestors=()):
        for node in body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                chain = ancestors + (node,)
                (classes if isinstance(node, ast.ClassDef) else functions).append(chain)
                walk(node.body, chain)
    walk(tree.body)
    candidates = [c for c in functions if '.'.join(n.name for n in c) == symbol]
    if not candidates and '.' not in symbol:
        candidates = [c for c in functions if c[-1].name == symbol]
    # A property setter shares a name with its getter. Keep the getter as target.
    if len(candidates) > 1:
        getters = [c for c in candidates if not any(isinstance(d, ast.Attribute)
            and d.attr in ('setter', 'deleter') for d in c[-1].decorator_list)]
        if len(getters) == 1: candidates = getters
    if len(candidates) != 1:
        raise ValueError('API target missing or lexically ambiguous: ' + symbol)
    chain = candidates[0]
    target = chain[-1]
    aliases = {'property': 'property', 'staticmethod': 'staticmethod', 'classmethod': 'classmethod'}
    for item in tree.body:
        if isinstance(item, ast.ImportFrom) and item.module == 'builtins':
            for alias in item.names:
                if alias.name in ('property', 'staticmethod', 'classmethod'):
                    aliases[alias.asname or alias.name] = alias.name
        elif isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            aliases.pop(item.name, None)
        elif isinstance(item, (ast.Assign, ast.AnnAssign)):
            for part in ast.walk(item):
                if isinstance(part, ast.Name) and isinstance(part.ctx, ast.Store): aliases.pop(part.id, None)
        elif isinstance(item, ast.ImportFrom) and any(a.name == '*' for a in item.names):
            aliases.clear()
        elif isinstance(item, (ast.Import, ast.ImportFrom)):
            for alias in item.names: aliases.pop(alias.asname or alias.name.split('.')[0], None)

    def member_kind(node, owner):
        owner_bindings = {n.name for n in owner.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}
        owner_bindings.update(n.id for item in owner.body if isinstance(item, (ast.Assign, ast.AnnAssign))
                              for n in ast.walk(item) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store))
        kinds = [aliases.get(d.id) for d in node.decorator_list
                 if isinstance(d, ast.Name) and d.id not in owner_bindings]
        if 'property' in kinds: return 'property'
        if 'staticmethod' in kinds: return 'staticmethod'
        if 'classmethod' in kinds: return 'classmethod'
        return 'method' if not node.decorator_list else 'unknown_decorated_member'

    owner = chain[-2] if len(chain) > 1 and isinstance(chain[-2], ast.ClassDef) else None
    containing_class = next((n for n in reversed(chain[:-1]) if isinstance(n, ast.ClassDef)), None)
    lexical_parents = [n for n in chain[:-1] if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    evidence = dict(policy=POLICY, file=str(path.relative_to(root)), source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        target=dict(symbol='.'.join(n.name for n in chain), signature=_signature(target),
                    kind=member_kind(target, owner) if owner is not None else 'function',
                    module_level_importable=len(chain) == 1),
        classes=[], omitted=[], chars=0, scope='Static declarations/API shape only; no observed outputs or oracle values')
    if owner is not None:
        kind=member_kind(target, owner)
        if kind=='property': evidence['target']['access']='instance.'+target.name
        elif kind=='method': evidence['target']['access']='instance.'+target.name+'(...)'
        elif kind in ('staticmethod','classmethod'): evidence['target']['access']=owner.name+'.'+target.name+'(...)'
    if lexical_parents:
        loads = {n.id for n in ast.walk(target) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}
        outer_bindings = set().union(*(_bindings(n) for n in lexical_parents))
        evidence['target']['closure_variables'] = sorted((loads - _bindings(target)) & outer_bindings)
        public_index=next(i for i,n in enumerate(chain[:-1]) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)))
        public=chain[public_index]
        public_owner=chain[public_index-1] if public_index and isinstance(chain[public_index-1],ast.ClassDef) else None
        evidence['enclosing_api'] = dict(symbol='.'.join(n.name for n in chain[:public_index+1]),
            kind=member_kind(public,public_owner) if public_owner is not None else 'function',
            signature=_signature(public),
            source=ast.get_source_segment(source, public),
            note='Nested function is not a module-level import. Obtain it through the enclosing production API; do not reimplement it.')
    referenced = {n.id for n in ast.walk(target) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}
    relevant = [c for c in classes if c[-1] is containing_class or len(c) == 1 and c[-1].name in referenced]
    relevant.sort(key=lambda c: c[-1] is not containing_class)
    for c in relevant[:3]:
        node = c[-1]
        members = []
        for item in node.body:
            if not isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)): continue
            if any(isinstance(d, ast.Attribute) and d.attr in ('setter', 'deleter') for d in item.decorator_list): continue
            members.append(dict(name=item.name, kind=member_kind(item, node), signature=_signature(item)))
        members.sort(key=lambda m: (m['name'] != target.name, m['kind'] != 'property', m['name']))
        evidence['classes'].append(dict(symbol='.'.join(n.name for n in c), members=members[:16],
                                      members_omitted=max(0, len(members)-16)))
    def size(): return len(json.dumps(evidence, ensure_ascii=False, separators=(',', ':')))
    if size() > max_chars and 'enclosing_api' in evidence:
        evidence['enclosing_api'].pop('source', None)
        evidence['omitted'].append('enclosing source excerpt')
    while size() > max_chars and any(c['members'] for c in evidence['classes']):
        row = next(c for c in reversed(evidence['classes']) if c['members'])
        if row['members'][-1]['name'] == target.name and len(row['members']) == 1: break
        row['members'].pop(); row['members_omitted'] += 1
    if size() > max_chars:
        raise ValueError('Essential API evidence exceeds the declared budget')
    for _ in range(3): evidence['chars'] = size()
    if size() > max_chars: raise ValueError('Essential API evidence exceeds the declared budget')
    return evidence


def augment_prompt(system, user, root, relative_file, symbol, enabled=False, max_chars=2500):
    """Same concise-file instructions in both arms; only evidence is the treatment."""
    system = system.rstrip() + '\n\n' + COMMON_INSTRUCTION
    evidence = None
    if enabled:
        evidence = build_api_contract(root, relative_file, symbol, max_chars=max_chars)
        user += '\n\nProduction API facts (override conflicting generated usage examples):\n'
        user += json.dumps(evidence, ensure_ascii=False, separators=(',', ':'))
    return system, user, evidence
