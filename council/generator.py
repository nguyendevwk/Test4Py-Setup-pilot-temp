"""Test generation by Coder model (GPU 0)."""
from council.critic import clean_code_block

def generate_test_with_coder(
    engine,
    module_name: str,
    target_function: str,
    target_source: str,
    setup_context: str,
    scenario_desc: str = ""
) -> str:
    """Coder model (GPU 0) writes a complete pytest suite incorporating Verified Setup."""
    sys_prompt = """You are an expert Python QA Engineer specializing in writing robust pytest test suites.
You will write high-coverage unit tests for the specified Python function.

Requirements:
1. CORRECT IMPORTS: Import the required classes and functions correctly using real package modules.
2. STATE INITIALIZATION: Use the provided Verified Setup Context to construct and initialize objects before calling the target function.
3. MEANINGFUL ASSERTIONS: Validate return values, attribute updates, and state transitions. Do not write empty tests.
4. OUTPUT FORMAT: Output ONLY the complete test code inside a single ```python code block. No explanations."""

    user_prompt = f"""### Module Under Test: `{module_name}`
### Target Function: `{target_function}`

### Target Implementation Source Code:
```python
{target_source}
```

### Verified Object Setup Context:
```python
{setup_context}
```

### Scenario Specification:
{scenario_desc}

Generate a comprehensive pytest test file testing normal paths, edge cases, and verifying state transitions."""

    raw_response = engine.call_coder(sys_prompt, user_prompt)
    code = clean_code_block(raw_response)
    return code
