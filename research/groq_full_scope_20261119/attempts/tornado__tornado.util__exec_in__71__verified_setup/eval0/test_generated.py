import builtins
import types
import pytest
from tornado.util import exec_in

def test_exec_in_executes_string_and_sets_globals_and_locals():
    # Prepare globals and locals
    globals_dict = {"x": 1}
    locals_dict = {"y": 2}
    # Code string that modifies globals and locals
    code_str = """
x = x + 10
y = y * 3
z = 42
"""
    exec_in(code_str, globals_dict, locals_dict)
    # Global 'x' should be updated
    assert globals_dict["x"] == 11
    # Local 'y' should be updated
    assert locals_dict["y"] == 6
    # New local 'z' should be added to locals
    assert locals_dict["z"] == 42
    # 'z' should not appear in globals
    assert "z" not in globals_dict

def test_exec_in_executes_code_object_and_respects_dont_inherit():
    # Compile a code object that uses a name defined in the caller's globals
    caller_globals = {"a": 5}
    code_obj = compile("b = a + 1", "<string>", "exec", dont_inherit=True)
    # Execute with empty globals to ensure 'a' is not inherited
    exec_in(code_obj, {}, None)
    # 'b' should be defined in the empty globals dict
    assert "b" in globals()
    # The value of 'b' should be 6 (5 + 1)
    assert globals()["b"] == 6
    # Clean up the global we added
    del globals()["b"]

def test_exec_in_raises_type_error_for_invalid_code_type():
    # Passing an unsupported type should raise a TypeError
    with pytest.raises(TypeError):
        exec_in(12345, {}, None)
