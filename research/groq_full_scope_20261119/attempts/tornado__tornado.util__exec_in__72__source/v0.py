import builtins
import types
import pytest
from tornado.util import exec_in

def test_exec_in_string_executes_and_modifies_globals():
    # Prepare a global dictionary and a local dictionary
    globals_dict = {"x": 1}
    locals_dict = {"y": 2}
    # Code string that modifies both globals and locals
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
    # New variable 'z' should appear in globals (exec uses globals as default for new names)
    assert globals_dict["z"] == 42
    # Ensure that builtins are still accessible
    assert builtins.len([1, 2, 3]) == 3

def test_exec_in_code_object_executes_and_uses_locals():
    # Compile a code object that defines a function and uses locals
    code_obj = compile(
        """
def add(a, b):
    return a + b
result = add(5, 7)
""",
        "<string>",
        "exec",
        dont_inherit=True,
    )
    globals_dict = {}
    locals_dict = {}
    exec_in(code_obj, globals_dict, locals_dict)
    # The function should be defined in globals
    assert "add" in globals_dict
    assert isinstance(globals_dict["add"], types.FunctionType)
    # The result should be stored in locals
    assert locals_dict["result"] == 12
    # Ensure that the function can be called from globals
    assert globals_dict["add"](3, 4) == 7

def test_exec_in_raises_on_invalid_code():
    globals_dict = {}
    locals_dict = {}
    # Passing an object that is neither str nor code object should raise TypeError
    with pytest.raises(TypeError):
        exec_in(42, globals_dict, locals_dict)
    # Passing a code object that raises an exception should propagate that exception
    bad_code = compile("raise ValueError('bad')", "<string>", "exec", dont_inherit=True)
    with pytest.raises(ValueError, match="bad"):
        exec_in(bad_code, globals_dict, locals_dict)
