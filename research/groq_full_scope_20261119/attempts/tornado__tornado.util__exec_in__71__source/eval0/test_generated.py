import builtins
import types
import pytest
from tornado.util import exec_in

def test_exec_in_executes_string_and_sets_globals_and_locals():
    # Prepare globals and locals
    globals_dict = {}
    locals_dict = {}
    # Code string that defines a variable and uses a built-in
    code_str = """
x = 10
y = sum([1, 2, 3])
"""
    exec_in(code_str, globals_dict, locals_dict)
    # The globals should contain the defined names
    assert globals_dict["x"] == 10
    assert globals_dict["y"] == 6
    # The locals should be the same as globals when provided
    assert locals_dict is globals_dict

def test_exec_in_executes_compiled_code_object_and_shares_namespace():
    # Compile a code object that modifies a global variable
    code_obj = compile("z = 42", "<string>", "exec", dont_inherit=True)
    globals_dict = {}
    exec_in(code_obj, globals_dict)
    # The global variable should be set
    assert globals_dict["z"] == 42

def test_exec_in_raises_type_error_for_invalid_code_argument():
    # Passing an unsupported type should raise a TypeError
    with pytest.raises(TypeError):
        exec_in(123, {}, {})
