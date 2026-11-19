import pytest
from pycg.machinery.definitions import DefinitionManager, DefinitionError
import pycg.machinery.utils as utils

def test_handle_function_def_creates_and_returns_definition():
    manager = DefinitionManager()

    # First call should create function and return definitions
    fn_def = manager.handle_function_def('pkg', 'func')
    full_ns = utils.join_ns('pkg', 'func')
    assert fn_def.get_ns() == full_ns
    assert fn_def.get_type() == utils.constants.FUN_DEF
    assert hasattr(fn_def, 'decorator_names')
    assert isinstance(fn_def.decorator_names, set)

    return_ns = utils.join_ns(full_ns, utils.constants.RETURN_NAME)
    ret_def = manager.get(return_ns)
    assert ret_def is not None
    assert ret_def.get_type() == utils.constants.NAME_DEF

    # Subsequent call should return the same function definition without duplication
    fn_def2 = manager.handle_function_def('pkg', 'func')
    assert fn_def2 is fn_def

    # The manager should contain exactly two definitions
    defs = manager.get_defs()
    assert set(defs.keys()) == {full_ns, return_ns}
