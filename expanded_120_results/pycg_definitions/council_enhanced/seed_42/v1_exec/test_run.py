import pytest
from pycg.machinery.definitions import DefinitionManager, Definition, DefinitionError
from pycg.machinery import utils

def test_assign_creates_return_pointer_and_merges():
    dm = DefinitionManager()

    # Create a function definition and add a name pointer entry
    func_def = Definition('pkg.mod.func', utils.constants.FUN_DEF)
    func_def.get_name_pointer().add('pkg.mod.var')

    # Assign the function definition to the manager
    returned_def = dm.assign('pkg.mod.func', func_def)

    # The returned object should be the same as the one stored
    assert returned_def is dm.get('pkg.mod.func')
    # The original name pointer entry should still be present
    assert 'pkg.mod.var' in returned_def.get_name_pointer().get()

    # A return pointer definition should have been created
    return_ns = utils.join_ns('pkg.mod.func', utils.constants.RETURN_NAME)
    assert return_ns in dm.defs
    return_def = dm.get(return_ns)
    # The return definition should be of type NAME_DEF
    assert return_def.get_type() == utils.constants.NAME_DEF
    # Its name pointer should contain the fully qualified return name
    expected_return_name = utils.join_ns('pkg.mod.func', utils.constants.RETURN_NAME)
    assert expected_return_name in return_def.get_name_pointer().get()

    # Now test assigning a non-function definition does not create a return pointer
    non_func_def = Definition('pkg.mod.var', utils.constants.NAME_DEF)
    dm.assign('pkg.mod.var', non_func_def)
    # No return namespace should exist for the non-function definition
    non_func_return_ns = utils.join_ns('pkg.mod.var', utils.constants.RETURN_NAME)
    assert non_func_return_ns not in dm.defs
