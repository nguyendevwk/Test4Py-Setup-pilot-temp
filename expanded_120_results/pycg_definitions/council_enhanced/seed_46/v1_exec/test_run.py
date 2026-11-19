import pytest
from pycg.machinery.definitions import DefinitionManager, DefinitionError
from pycg.machinery import utils

def test_handle_function_def_creates_and_links_return_pointer():
    dm = DefinitionManager()
    parent_ns = "pkg.mod"
    fn_name = "func"

    # First call should create the function definition and its return pointer
    fn_def = dm.handle_function_def(parent_ns, fn_name)
    assert fn_def.get_type() == utils.constants.FUN_DEF
    full_ns = utils.join_ns(parent_ns, fn_name)
    assert fn_def.get_ns() == full_ns

    return_ns = utils.join_ns(full_ns, utils.constants.RETURN_NAME)
    return_def = dm.get(return_ns)
    assert return_def is not None
    assert return_def.get_type() == utils.constants.NAME_DEF

    expected_return_name = utils.join_ns(full_ns, utils.constants.RETURN_NAME)
    assert expected_return_name in return_def.get_name_pointer().get()

    # Subsequent calls should return the same objects without duplication
    fn_def2 = dm.handle_function_def(parent_ns, fn_name)
    assert fn_def2 is fn_def
    assert dm.get(return_ns) is return_def
    assert len(dm.get_defs()) == 2
