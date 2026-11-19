import pytest
from pycg.machinery.definitions import DefinitionManager, DefinitionError
from pycg.machinery import constants

def test_assign_function_def_creates_return_pointer():
    dm = DefinitionManager()
    ns = 'pkg.mod.func'

    # Create a function definition
    func_def = dm.create(ns, constants.FUN_DEF)

    # Assign the same definition
    returned_def = dm.assign(ns, func_def)

    # The returned definition should be the function definition
    assert returned_def is dm.get(ns)
    assert returned_def.get_type() == constants.FUN_DEF

    # The return namespace is the function namespace joined with the return name
    return_ns = f"{ns}.{constants.RETURN_NAME}"
    return_def = dm.get(return_ns)

    # The return definition should exist and be a name definition
    assert return_def is not None
    assert return_def.get_type() == constants.NAME_DEF

    # The return definition's name pointer should contain the full return name
    expected_return_name = return_ns
    assert expected_return_name in return_def.get_name_pointer().get()
