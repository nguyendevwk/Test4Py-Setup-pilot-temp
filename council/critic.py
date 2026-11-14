"""Critic and Quality Assurance for Council Architecture."""
import ast
from typing import Dict, Any

def clean_code_block(raw: str) -> str:
    """Common deterministic extraction; never salvage/truncate ambiguous completions."""
    from pilot.quality import extract_code, final_answer
    answer, status = final_answer(raw)
    if not answer:
        raise ValueError('No complete final answer: '+status)
    return extract_code(answer).strip()


def audit_test_quality(code: str) -> Dict[str, Any]:
    """Syntactic screening only; this does not establish semantic correctness."""
    result = {
        "valid_ast": False,
        "test_functions": 0,
        "assertion_count": 0,
        "assertion_like_calls": 0,
        "is_hollow": False,
        "semantic_assertion_accuracy": None,
        "review_required": True,
        "tautological_assertions": 0,
        "error": None
    }
    try:
        tree = ast.parse(code)
        result["valid_ast"] = True
    except SyntaxError as e:
        result["error"] = f"SyntaxError: {e}"
        return result

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_"):
            result["test_functions"] += 1
        elif isinstance(node, ast.Assert):
            result["assertion_count"] += 1
            if isinstance(node.test, ast.Constant) and bool(node.test.value):
                result["tautological_assertions"] += 1

        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and (
            node.func.attr.startswith('assert') or node.func.attr in {'raises', 'warns'}):
            result['assertion_like_calls'] += 1

    if result["test_functions"] > 0 and result['assertion_like_calls'] == 0 and result["assertion_count"] == result["tautological_assertions"]:
        result["is_hollow"] = True

    return result


def repair_with_critic(
    engine,
    broken_code: str,
    traceback_log: str,
    target_source: str,
    setup_context: str
) -> str:
    """Critic model (GPU 1) analyzes runtime failure and produces a targeted fix."""
    sys_prompt = """Repair the pytest suite using production source and runtime diagnostics.
Preserve tested scenarios and meaningful assertions. Fix the root cause rather than
deleting tests, weakening checks, skipping tests, suppressing exceptions, or modifying
product code. Derive expectations from source, not from a desire to pass.
Return exactly one complete Python code block without explanation."""

    user_prompt = f"""### Target Source Code:
```python
{target_source}
```

### Setup Context (may be empty or unverified):
```python
{setup_context}
```

### Currently Broken Test Code:
```python
{broken_code}
```

### Pytest Failure Traceback:
```text
{traceback_log}
```

Please fix the imports, object initialization, and parameters so all tests execute cleanly and pass."""

    raw_response = engine.call_critic(sys_prompt, user_prompt)
    repaired_code = clean_code_block(raw_response)
    return repaired_code
