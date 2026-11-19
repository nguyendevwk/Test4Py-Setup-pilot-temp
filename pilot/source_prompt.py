"""Source-first development ablation; no model-generated usage claims or oracles."""
import ast
import copy
import json
from pathlib import Path

from pilot.api_contract import COMMON_INSTRUCTION, build_api_contract

POLICY = 'source-first-v2'


def trusted_context(root, relative_file, symbol, max_chars=10000):
    facts = build_api_contract(root, relative_file, symbol)
    source = (Path(root)/relative_file).read_text()
    tree = ast.parse(source)
    parts = facts['target']['symbol'].split('.')
    body = tree.body
    chain = []
    for name in parts:
        choices = [n for n in body if isinstance(n, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
                   and n.name == name and not any(isinstance(d, ast.Attribute)
                       and d.attr in ('setter', 'deleter') for d in getattr(n, 'decorator_list', []))]
        if len(choices) != 1:
            raise ValueError('Ambiguous source scope: '+name)
        chain.append(choices[0]); body = choices[0].body
    # Start with the complete top-level lexical owner, including decorators.
    owner = copy.deepcopy(chain[0])
    imports = [copy.deepcopy(n) for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))]
    render = lambda n: ast.unparse(ast.Module(body=imports+[n], type_ignores=[]))
    text = render(owner)
    scope = 'complete lexical owner plus module imports; AST-rendered production source'
    if len(text) > max_chars:
        # Keep the target path and constructors. Do not cut source mid-function.
        def prune(node, depth):
            result = copy.deepcopy(node)
            if depth < len(chain)-1:
                result.body = [prune(chain[depth+1], depth+1)]
                if isinstance(node, ast.ClassDef):
                    result.body = [copy.deepcopy(n) for n in node.body
                                   if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name=='__init__'] + result.body
            return result
        text = render(prune(chain[0], 0))
        scope = 'target lexical path, enclosing constructors and module imports; other members omitted'
    if len(text) > max_chars:
        raise ValueError('Trusted source context exceeds fixed character budget')
    return dict(policy=POLICY, source_sha256=facts['source_sha256'], file=str(relative_file),
                target=facts['target']['symbol'], scope=scope, code=text), facts


def source_first_prompt(system, root, relative_file, symbol, module, include_contract=False):
    context, facts = trusted_context(root, relative_file, symbol)
    system = system.rstrip()+'\n\n'+COMMON_INSTRUCTION
    user = ('Generate a concise, robust pytest file for the production target below.\n'
            'CRITICAL REQUIREMENTS:\n'
            '- Write EXACTLY ONE focused test function covering the primary behavior of the target.\n'
            '- Keep the entire file under 35 lines of Python code to strictly avoid truncation.\n'
            '- Explicitly import `pytest` and any necessary standard library modules at the top.\n'
            '- Import its public enclosing API when the target is nested.\n'
            '- Use the real implementation; mock external I/O only when needed, never the target itself.\n'
            '- Infer assertions from the production source.\n\n'
            'Module: '+module+'\nTarget: '+context['target']+'\n'
            'The following context is extracted from pinned production source. '
            'Model-generated summaries and usage examples have been replaced, because they may conflict '
            'with decorators or lexical ownership.\n'+context['scope']+'\n```python\n'+context['code']+'\n```')
    if include_contract:
        user += '\nStatic API facts:\n'+json.dumps(facts, ensure_ascii=False, separators=(',', ':'))
    return system, user, dict(context=context, contract=facts if include_contract else None)
