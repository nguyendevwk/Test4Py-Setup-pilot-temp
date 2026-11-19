import pytest
from pycg.machinery.definitions import DefinitionManager, DefinitionError
from pycg.machinery import utils

def test_handle_function_def_creates_and_returns_correct_definitions():
    manager = DefinitionManager()
    parent_ns = "module"
    fn_name = "foo"

    # First call creates function and return definitions
    defi = manager.handle_function_def(parent_ns, fn_name)
    full_ns = utils.join_ns(parent_ns, fn_name)
    assert defi.get_ns() == full_ns
    assert defi.get_type() == utils.constants.FUN_DEF

    return_ns = utils.join_ns(full_ns, utils.constants.RETURN_NAME)
    return_def = manager.get(return_ns)
    assert return_def is not None
    assert return_def.get_type() == utils.constants.NAME_DEF

    # Second call returns the same function definition and does not duplicate return def
    defi2 = manager.handle_function_def(parent_ns, fn_name)
    assert defi2 is defi
    assert manager.get(return_ns) is return_def

    # decorator_names is initialized as an empty set
    assert hasattr(defi, "decorator_names")
    assert isinstance(defi.decorator_names, set)

    # create should raise DefinitionError for invalid namespace
    with pytest.raises(DefinitionError):
        manager.create("", utils.constants.FUN_DEF)
    with pytest.raises(DefinitionError):
        manager.create(None, utils.constants.FUN_DEF)
