import builtins
import types
import pytest
from tornado.util import exec_in


def test_exec_in_executes_string_and_sets_variables(tmp_path):
    # Prepare a temporary file to be imported
    file_path = tmp_path / "temp_module.py"
    file_path.write_text("value = 42")

    # Code string that imports the temporary module and defines a variable
    code_str = f"""
import sys
sys.path.insert(0, r'{tmp_path}')
import temp_module
result = temp_module.value + 1
"""

    globals_dict = {}
    exec_in(code_str, globals_dict)

    # The executed code should have defined 'result' in the globals dict
    assert "result" in globals_dict
    assert globals_dict["result"] == 43
    # The temporary module should be importable from the globals dict
    assert "temp_module" in globals_dict
    assert globals_dict["temp_module"].value == 42


def test_exec_in_executes_code_object_and_uses_locals():
    # Create a code object that defines a local variable
    code_obj = compile("local_var = 99", "<string>", "exec", dont_inherit=True)

    globals_dict = {}
    locals_dict = {}
    exec_in(code_obj, globals_dict, locals_dict)

    # The local variable should be present in the locals dict
    assert locals_dict["local_var"] == 99
    # No globals should be modified
    assert globals_dict == {}


def test_exec_in_raises_on_invalid_code_type():
    # Passing an unsupported type (e.g., int) should raise a TypeError
    with pytest.raises(TypeError):
        exec_in(12345, {})
