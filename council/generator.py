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
    sys_prompt = """Write pytest tests from the supplied production source.
Use real imports and signatures; derive expected behavior from the source.
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
    return code
