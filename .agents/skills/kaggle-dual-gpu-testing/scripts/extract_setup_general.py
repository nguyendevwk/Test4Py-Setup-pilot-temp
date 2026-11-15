"""General AST State & Setup Miner for ANY Python Class/API.

This script parses any Python file, extracts class constructors, setters,
builders, and caller snippets, and formats candidate setup sequences.
"""
import ast
import itertools
from pathlib import Path
import sys

STATE_METHOD_PREFIXES = ('set_', 'add_', 'register_', 'create_', 'build_', 'init_', 'append_', 'put_', 'insert_')

def mine_class_state_methods(source_file: Path, class_name: str):
    tree = ast.parse(source_file.read_text())
    target_class = None
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            target_class = node
            break

    if not target_class:
        raise ValueError(f"Class '{class_name}' not found in {source_file}")

    state_methods = []
    for item in target_class.body:
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            name = item.name
            if name.startswith(STATE_METHOD_PREFIXES) or name in {'__init__'}:
                args = [arg.arg for arg in item.args.args if arg.arg != 'self']
                state_methods.append({
                    'name': name,
                    'args': args,
                    'is_init': name == '__init__'
                })
    return state_methods

def mine_call_sites(project_root: Path, class_name: str):
    call_evidence = []
    for py_file in project_root.rglob("*.py"):
        if any(part in {'tests', 'test', '.git', '__pycache__', 'venv'} for part in py_file.parts):
            continue
        try:
            tree = ast.parse(py_file.read_text())
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                    call_evidence.append({
                        'method': node.func.attr,
                        'file': str(py_file.relative_to(project_root)),
                        'line': node.lineno
                    })
        except Exception:
            continue
    return call_evidence

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python extract_setup_general.py <path_to_py_file> <class_name>")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    target_class = sys.argv[2]
    methods = mine_class_state_methods(file_path, target_class)
    print(f"🔍 Discovered state methods for '{target_class}':")
    for m in methods:
        print(f"  - {m['name']}({', '.join(m['args'])})")
