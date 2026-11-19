"""Test generation by Coder model (GPU 0)."""
import ast
import builtins
import sys
from council.critic import clean_code_block


def auto_resolve_imports(code: str, module_name: str, target_source: str) -> str:
    """General AST-based symbol resolver: automatically completes missing standard library

    and target-module imports for undefined names, preventing brittle NameError across any project.
    """
    try:
        tree = ast.parse(code)
    except Exception:
        return code

    # 1. Collect all defined and imported names in the test code
    defined = set(dir(builtins))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported.add(alias.asname or alias.name)
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imported.add(alias.asname or alias.name)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            defined.add(node.name)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            defined.add(node.id)

    # 2. Collect used names (loads)
    used = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            used.add(node.id)

    undefined = used - defined - imported
    if not undefined:
        return code

    # 3. Extract top-level exported symbols from target module AST
    target_exports = set()
    try:
        src_tree = ast.parse(target_source)
        for node in src_tree.body:
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                target_exports.add(node.name)
    except Exception:
        pass

    # 4. Deterministically resolve missing imports
    new_imports = []
    if "pytest" in undefined and "pytest" not in imported:
        new_imports.append("import pytest")
        undefined.discard("pytest")

    # Standard library modules (os, sys, json, re, math, time, shutil, socket, etc.)
    stdlib_modules = getattr(sys, "stdlib_module_names", set())
    stdlib_to_import = [name for name in sorted(undefined) if name in stdlib_modules]
    for m in stdlib_to_import:
        new_imports.append(f"import {m}")
        undefined.discard(m)

    # Common unittest.mock symbols
    mock_symbols = [s for s in ('Mock', 'MagicMock', 'patch', 'call') if s in undefined]
    if mock_symbols:
        new_imports.append(f"from unittest.mock import {', '.join(sorted(mock_symbols))}")
        for s in mock_symbols:
            undefined.discard(s)

    # Target module exported classes/exceptions/functions
    target_symbols = [s for s in sorted(undefined) if s in target_exports]
    if target_symbols and module_name:
        new_imports.append(f"from {module_name} import {', '.join(target_symbols)}")

    if not new_imports:
        return code

    return "\n".join(new_imports) + "\n" + code


def generate_test_with_coder(
    engine,
    module_name: str,
    target_function: str,
    target_source: str,
    setup_context: str,
    scenario_desc: str = ""
) -> str:
    """Coder model (GPU 0) writes a complete pytest suite incorporating Verified Setup."""
    sys_prompt = """Write pytest tests from the supplied production source.
Use real imports and signatures; derive expected behavior from the source.
Ensure all referenced classes, exceptions, and standard library modules are properly imported.
Setup examples guide input construction, not assertion oracles. Exercise the requested
scenarios and assert observable behavior. Do not use tautologies, skip tests, suppress
failures, or modify product code. Return one complete Python code block only."""

    user_prompt = f"""### Module Under Test: `{module_name}`
### Target Function: `{target_function}`

### Target Implementation Source Code:
```python
{target_source}
```

### Setup Context (may be empty or unverified):
```python
{setup_context}
```

### Scenario Specification:
{scenario_desc}

Generate a comprehensive pytest test file testing normal paths, edge cases, and verifying state transitions."""

    raw_response = engine.call_coder(sys_prompt, user_prompt)
    code = clean_code_block(raw_response)
    # Apply deterministic symbol resolution for any general Python codebase
    code = auto_resolve_imports(code, module_name, target_source)
    return code
