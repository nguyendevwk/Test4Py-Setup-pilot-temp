"""Audited adapters for pinned Test4Py. No expected outputs or mutant feedback.

Common runtime compatibility: CPU embeddings and empty-vector-query handling.
Improved arm: verified class declarations/member compatibility and stdlib imports.
"""
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import types

from pilot.common import append_json, command
from pilot.multitarget import checkout_env, inspect_api


def load_cpu_embedding(upstream):
    """Execute unchanged embedding source except one explicit device assignment.

    Patch the module AST in memory, never the checkout. Other CUDA users are not
    monkeypatched. Both arms get this same hardware-only adaptation.
    """
    path = Path(upstream)/'test4dt/embedding.py'
    source = path.read_text()
    tree = ast.parse(source)
    changes = []
    class CPU(ast.NodeTransformer):
        def visit_Assign(self, node):
            if any(isinstance(t, ast.Attribute) and isinstance(t.value, ast.Name)
                   and t.value.id == 'self' and t.attr == 'device' for t in node.targets):
                changes.append(node.lineno)
                node.value = ast.Call(func=ast.Attribute(value=ast.Name(id='torch', ctx=ast.Load()), attr='device', ctx=ast.Load()),
                                      args=[ast.Constant('cpu')], keywords=[])
            return self.generic_visit(node)
    tree = CPU().visit(tree)
    if len(changes) != 1:
        raise ValueError('Unsupported embedding source: expected exactly one device assignment')
    ast.fix_missing_locations(tree)
    module = types.ModuleType('test4dt.embedding')
    module.__file__, module.__package__ = str(path), 'test4dt'
    module.__spec__ = importlib.util.spec_from_file_location(module.__name__, path)
    sys.modules[module.__name__] = module
    try:
        exec(compile(tree, str(path), 'exec'), module.__dict__)
    except BaseException:
        sys.modules.pop(module.__name__, None)
        raise
    original = module.find_topK_message
    def nonempty(name, messages, query_vector, k=1):
        return original(name, messages, query_vector, k) if messages else []
    module.find_topK_message = nonempty
    return dict(policy='cpu-embedding-and-empty-query-v1', source_sha256=hashlib.sha256(source.encode()).hexdigest(),
                patched_device_lines=changes, embedding_device=str(module.embedder.device))


def stdlib_import_patch(code):
    """Repair missing `module.attribute` names only when the module is in stdlib.

    No third-party provider guessing, no expressions/assertions modified. Shadowed
    names are left alone. This is a deterministic intervention, not a model pass.
    """
    try:
        tree = ast.parse(code)
        compile(tree, '<candidate>', 'exec')
    except SyntaxError:
        return code, []
    bound = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Name) and isinstance(n.ctx, (ast.Store, ast.Param)):
            bound.add(n.id)
        elif isinstance(n, ast.arg):
            bound.add(n.arg)
        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            bound.add(n.name)
        elif isinstance(n, ast.Import):
            bound.update(a.asname or a.name.split('.')[0] for a in n.names)
        elif isinstance(n, ast.ImportFrom):
            bound.update(a.asname or a.name for a in n.names)
    modules = sorted({n.value.id for n in ast.walk(tree) if isinstance(n, ast.Attribute)
                      and isinstance(n.value, ast.Name) and n.value.id not in bound
                      and n.value.id in sys.stdlib_module_names and not n.value.id.startswith('_')})
    if not modules:
        return code, []
    # Import must follow the module docstring and any __future__ statements.
    position = 0
    for n in tree.body:
        if isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant) and isinstance(n.value.value, str) and position == 0:
            position = n.end_lineno
        elif isinstance(n, ast.ImportFrom) and n.module == '__future__':
            position = n.end_lineno
        else:
            break
    lines = code.splitlines(keepends=True)
    patched = ''.join(lines[:position])+''.join('import '+name+'\n' for name in modules)+''.join(lines[position:])
    return patched, modules


def validate_imports(code, root, timeout=15):
    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        return dict(status='syntax_error', accepted=False, error=str(exc))
    imports = [ast.unparse(n) for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))]
    if not imports:
        return dict(status='no_direct_imports', accepted=True, imports=[])
    # Only imported MODULE namespaces are checked. Instance attributes and
    # dynamic module __getattr__ cases remain unknown, never invented facts.
    aliases = set()
    for n in tree.body:
        if isinstance(n, ast.Import):
            aliases.update(a.asname or a.name.split('.')[0] for a in n.names)
        elif isinstance(n, ast.ImportFrom):
            aliases.update(a.asname or a.name for a in n.names)
    shadowed = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store)}
    shadowed.update(n.arg for n in ast.walk(tree) if isinstance(n, ast.arg))
    checks = sorted({ast.unparse(n) for n in ast.walk(tree) if isinstance(n, ast.Attribute)
                     and isinstance(n.value, ast.Name) and n.value.id in aliases-shadowed})
    script = '\n'.join(imports)+"\n"+f"""
import inspect as _inspect, types as _types, json as _json
_unknown = []
for _expression in {checks!r}:
    _name, _attribute = _expression.split('.', 1)
    _object = globals()[_name]
    if not isinstance(_object, _types.ModuleType):
        continue
    try:
        _inspect.getattr_static(_object, _attribute)
    except AttributeError:
        if '__getattr__' in vars(_object):
            _unknown.append(_expression)
        else:
            raise AttributeError('Contradicted imported module attribute: '+_expression)
print(_json.dumps(dict(unknown=_unknown)))
"""
    process = command([sys.executable, '-c', script], cwd=root,
                      env=checkout_env(root), timeout=timeout)
    accepted=process['returncode'] == 0 and not process['timeout']
    try:
        unknown=json.loads(process['stdout'].splitlines()[-1])['unknown'] if accepted else []
    except (ValueError, IndexError, KeyError):
        unknown=[]
    return dict(status='verified_imports_attributes_unknown' if accepted and unknown else 'verified' if accepted else 'contradicted',
                accepted=accepted, imports=imports, module_attribute_checks=checks, unknown_attributes=unknown,
                scope='direct imports and unshadowed module.attribute presence; dynamic/instance behavior not proven', process=process)


def install_type_guards(message, root, work):
    """Keep upstream inference/RAG; constrain candidates and replace usage fantasies.

    Summaries/semantic queries still come from the same SLM. Static full_members
    may be incomplete for dynamic Python; rejected candidates remain in audit logs.
    """
    root, work = Path(root), Path(work)
    original_filter = message.ArgMessage.filter_by_members
    original_usage = message.ClassMessage.get_how_to_use
    cache = {}
    def fact(cls):
        key = cls.full_name
        if key not in cache:
            try:
                payload = inspect_api(root, cls.file.mod_name, cls.class_name, timeout=15)
                cache[key] = dict(status='verified_declaration', api=payload)
            except Exception as exc:
                cache[key] = dict(status='unknown', error=repr(exc))
            append_json(work/'type_facts.jsonl', dict(candidate=key, **cache[key]))
        return cache[key]
    def filtered(param):
        candidates = original_filter(param)
        required = set(param.members)-set(dir(object))
        kept = [c for c in candidates if required <= set(c.full_members) and fact(c)['status'] == 'verified_declaration']
        append_json(work/'type_filter.jsonl', dict(parameter=param.name, required=sorted(required),
                    candidates=[c.full_name for c in candidates], retained=[c.full_name for c in kept],
                    limitation='strict declared members; dynamic members may be false negatives'))
        return kept
    def usage(cls):
        evidence = fact(cls)
        if evidence['status'] != 'verified_declaration':
            return 'Unverified candidate declaration; do not invent imports or constructor arguments.'
        api = evidence['api']
        # No model-generated how_to_use examples become trusted context.
        source = ast.get_source_segment(Path(cls.file.file_path).read_text(), cls.node) or ''
        if len(source) > 6000:
            source = cls.class_code+'\n'+(cls.init_method.code if cls.init_method is not None else '')
        return json.dumps(dict(provenance='production declaration + actual module import/signature',
                   module=cls.file.mod_name, symbol=cls.class_name, signature=api['signature'],
                   declared_members=sorted(cls.full_members), source=source,
                   scope='declaration facts only; no observed returns or verified behavioral summary'))
    message.ArgMessage.filter_by_members = filtered
    message.ClassMessage.get_how_to_use = usage
    return dict(policy='verified-type-context-v1', original_filter=original_filter, original_usage=original_usage)


def tolerate_empty_pytest_report(testcase_module):
    """Common compatibility fix: collection failure remains failure, not KeyError.

    Only replace pytest_report['tests'] with get('tests', []) in the pinned method.
    Do not change budgets, diagnostics, test outcomes or repair decisions.
    """
    import inspect
    import textwrap
    source=textwrap.dedent(inspect.getsource(testcase_module.Testcase.find_assert_error))
    tree=ast.parse(source);changes=[]
    class Safe(ast.NodeTransformer):
        def visit_Subscript(self,node):
            if isinstance(node.value,ast.Name) and node.value.id=='pytest_report' and isinstance(node.slice,ast.Constant) and node.slice.value=='tests':
                changes.append(node.lineno)
                return ast.copy_location(ast.Call(func=ast.Attribute(value=node.value,attr='get',ctx=ast.Load()),
                                  args=[ast.Constant('tests'),ast.List(elts=[],ctx=ast.Load())],keywords=[]),node)
            return self.generic_visit(node)
    tree=Safe().visit(tree)
    if len(changes)!=1:
        raise ValueError('Unsupported upstream pytest report reader')
    ast.fix_missing_locations(tree)
    namespace={}
    exec(compile(tree,'<audited-upstream-report-adapter>','exec'),testcase_module.__dict__,namespace)
    testcase_module.Testcase.find_assert_error=namespace['find_assert_error']
    return dict(policy='collection-error-without-tests-key-v1',source_sha256=hashlib.sha256(source.encode()).hexdigest())
