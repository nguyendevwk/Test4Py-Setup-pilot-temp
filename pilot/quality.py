"""Common output protocol and source evidence, never expected outputs or oracles."""
import ast
import re


def final_answer(raw):
    if '</think>' in raw:
        return raw.rsplit('</think>', 1)[1].strip(), 'reasoning_removed'
    if '<think>' in raw:
        return '', 'incomplete_reasoning'
    return raw.strip(), 'plain'


def extract_code(text):
    blocks = re.findall(r'^```(?:python|py)?[ \t]*\n(.*?)^```[ \t]*$', text, re.M | re.S)
    if len(blocks) == 1:
        return '\n' + blocks[0].strip() + '\n'
    if '```' in text:
        raise ValueError('Expected one complete Python block; ambiguous or incomplete model response')
    return '\n' + text.strip() + '\n'


def code_quality(code):
    try:
        tree = ast.parse(code)
        return dict(ast_parse=True, assertions=sum(isinstance(n, ast.Assert) for n in ast.walk(tree)))
    except SyntaxError as exc:
        return dict(ast_parse=False, parse_error=str(exc), assertions=None)


def source_context(root):
    path = root / 'pycg/machinery/imports.py'
    source = path.read_text()
    tree = ast.parse(source)
    nodes = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom)) or
             isinstance(n, ast.FunctionDef) and n.name == 'get_custom_loader']
    manager = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'ImportManager')
    names = {'__init__','create_node','get_node','create_edge','set_current_mod','set_filepath'}
    nodes += [n for n in manager.body if isinstance(n, ast.FunctionDef) and n.name in names]
    parts = [f'pycg/machinery/imports.py:{n.lineno}\n{ast.get_source_segment(source,n)}' for n in nodes]
    return ('Authoritative production excerpts below override any conflicting model-generated examples. '
            'Use actual imports and signatures; distinguish a returned class from its instance. '
            'Do not invent modules or public classes. Derive assertions from production behavior.\n' + '\n\n'.join(parts))
