"""Critic and Quality Assurance for Council Architecture."""
import ast
import re
from typing import Dict, Any, Tuple

def clean_code_block(raw: str) -> str:
    """Extract strictly valid Python code from raw LLM output, stripping markdown and <think> tags."""
    # 1. Remove reasoning / think tags if present
    text = re.sub(r'<think>.*?</think>', '', raw, flags=re.DOTALL)
    text = text.strip()

    # 2. Extract from markdown code fence
    match = re.search(r'```(?:python)?\s*\n(.*?)\n```', text, re.DOTALL | re.IGNORECASE)
    if match:
        code = match.group(1).strip()
    else:
        # If no code fence, strip any leading/trailing explanatory text
        lines = []
        for line in text.splitlines():
            if line.startswith('```'):
                continue
            lines.append(line)
        code = '\n'.join(lines).strip()

    # 3. Quick AST sanity check
    try:
        ast.parse(code)
        return code
    except SyntaxError:
        # Fallback to searching first line starting with import or def
        all_lines = text.splitlines()
        code_lines = []
        in_code = False
        for l in all_lines:
            if l.startswith(('import ', 'from ', 'def test_', 'class Test', '@pytest.')):
                in_code = True
            if in_code:
                if l.startswith('```'):
                    break
                code_lines.append(l)
        candidate = '\n'.join(code_lines).strip()
        try:
            ast.parse(candidate)
            return candidate
        except Exception:
            return code


def audit_test_quality(code: str) -> Dict[str, Any]:
    """Audit syntactic validity and semantic assertion presence."""
    result = {
        "valid_ast": False,
        "test_functions": 0,
        "assertion_count": 0,
        "is_hollow": False,
        "error": None
    }
    try:
        tree = ast.parse(code)
        result["valid_ast"] = True
    except SyntaxError as e:
        result["error"] = f"SyntaxError: {e}"
        return result

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
            result["test_functions"] += 1
        elif isinstance(node, ast.Assert):
            result["assertion_count"] += 1

    if result["test_functions"] > 0 and result["assertion_count"] == 0:
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
    sys_prompt = """You are a Principal Software Quality Engineer and Test Repair Specialist.
Your goal is to fix the failing pytest test cases based on the provided runtime traceback.

Rules:
1. PRESERVE ASSERTIONS: Never remove or comment out failing assertions. Fix the root cause instead.
2. USE THE SETUP CONTEXT: Ensure the state of the object is properly initialized as specified in Setup Context.
3. OUTPUT FORMAT: Return ONLY the complete, corrected Python pytest file inside a single ```python code block. No explanations."""

    user_prompt = f"""### Target Source Code:
```python
{target_source}
```

### Verified Setup Context:
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
