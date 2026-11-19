import builtins
import types
import pytest
from tornado.util import exec_in

def test_exec_in_string_modifies_globals():
    """exec_in should execute a string and modify the provided globals."""
    globals_dict = {}
    code_str = "x = 42\nprint('hello')"
    exec_in(code_str, globals_dict)
    assert "x" in globals_dict
    assert globals_dict["x"] == 42
    # The print statement should have written to stdout; we don't capture it here.

def test_exec_in_code_object_with_loc():
    """exec_in should execute a code object and use the provided locals."""
    globals_dict = {}
    locals_dict = {}
    code_obj = compile("y = 99", "<string>", "exec", dont_inherit=True)
    exec_in(code_obj, globals_dict, locals_dict)
    assert "y" in locals_dict
    assert locals_dict["y"] == 99
    assert "y" not in globals_dict  # locals are separate

def test_exec_in_invalid_code_raises():
    """exec_in should raise a SyntaxError when given invalid code."""
    globals_dict = {}
    invalid_code = "def bad_func(:\n    pass"
    with pytest.raises(SyntaxError):
        exec_in(invalid_code, globals_dict)
