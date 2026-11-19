import json
import subprocess
from pathlib import Path
from council.groq_engine import GroqCouncilEngine
from pilot.multitarget import clean_code_block

engine = GroqCouncilEngine()

broken_code = """import pytest
from typesystem.fields import String, Integer, OneOf
from typesystem.base import ValidationError

def test_oneof_exact_match_and_errors():
    schema = OneOf([String(), Integer()])
    val, err = schema.validate_or_error("sample_text")
    assert err is None
    assert val == "sample_text"

    val, err = schema.validate_or_error(42)
    assert err is None
    assert val == 42

    multi_schema = OneOf([String(), String()])
    with pytest.raises(ValidationError) as excinfo:
        multi_schema.validate("dup")
    assert excinfo.value.code == "multiple_matches"
"""

traceback_log = """
______________________ test_oneof_exact_match_and_errors _______________________
    with pytest.raises(ValidationError) as excinfo:
        multi_schema.validate("dup")
>   assert excinfo.value.code == "multiple_matches"
E   AttributeError: 'ValidationError' object has no attribute 'code'
"""

sys_prompt = """Repair the pytest test code so that all tests pass.
IMPORTANT: Note that ValidationError in typesystem does NOT have a .code attribute directly on the exception instance.
To check the error message or code, either check str(excinfo.value) or iterate over excinfo.value.messages() (each message has .code and .text).
Return only the complete Python code block."""

user_prompt = f"""### Broken Test Code:
```python
{broken_code}
```

### Pytest Error:
```text
{traceback_log}
```

Please repair line 22 so all assertions succeed."""

resp = engine.call_critic(sys_prompt, user_prompt)
cleaned = clean_code_block(resp)
print("=== REPAIRED CODE ===")
print(cleaned)

# Now test execute it with pytest!
test_file = Path("/tmp/test_oneof_repaired.py")
test_file.write_text(cleaned)

cmd = ["uv", "run", "--with", "pytest", "python3", "-m", "pytest", str(test_file)]
env = dict(PYTHONPATH="local_benchmark_repos/typesystem", PATH=os.environ["PATH"])
res = subprocess.run(cmd, capture_output=True, text=True, env=env)
print("=== PYTEST RESULT ===")
print("Exit code:", res.returncode)
print(res.stdout[-500:])
if res.stderr:
    print("Stderr:", res.stderr[-500:])
