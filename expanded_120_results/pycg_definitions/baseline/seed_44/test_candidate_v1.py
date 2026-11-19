import pytest
from pycg.machinery.definitions import DefinitionManager, Definition
from pycg.machinery import utils

def test_handle_function_def_creates_and_reuses_definitions():
    mgr = DefinitionManager()
    parent_ns = "pkg"
    fn_name = "func"

    # First call: should create function and return definitions
    func_def = mgr.handle_function_def(parent_ns, fn_name)
    assert isinstance(func_def, Definition)
    full_ns = utils.join_ns(parent_ns, fn_name)
    assert func_def.get_ns() == full_ns
    assert func_def.get_type() == utils.constants.FUN_DEF
    assert hasattr(func_def, "decorator_names") and func_def.decorator_names == set()

    return_ns = utils.join_ns(full_ns, utils.constants.RETURN_NAME)
    return_def = mgr.get(return_ns)
    assert return_def is not None
    assert return_def.get_type() == utils.constants.NAME_DEF

    # Second call with same names: should return same objects and not duplicate
    func_def2 = mgr.handle_function_def(parent_ns, fn_name)
    assert func_def2 is func_def
    assert mgr.get(return_ns) is return_def
    assert len(mgr.get_defs()) == 2  # only function and return defs

    # Call with a different function: should add new defs
    fn_name2 = "func2"
    func_def3 = mgr.handle_function_def(parent_ns, fn_name2)
    assert func_def3.get_ns() == utils.join_ns(parent_ns, fn_name2)
    assert func_def3.get_type() == utils.constants.FUN_DEF
    assert len(mgr.get_defs()) == 4  # two functions + two returns
