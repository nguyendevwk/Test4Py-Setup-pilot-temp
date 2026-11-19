import pytest
from pycg.machinery.definitions import DefinitionManager, Definition
from pycg.machinery import utils

def test_assign_creates_return_pointer_and_merges():
    dm = DefinitionManager()
    ns = 'pkg.mod.func'
    # Create a function definition manually and add a name pointer
    func_def = Definition(ns, utils.constants.FUN_DEF)
    func_def.get_name_pointer().add('pkg.mod.other')
    # Assign the definition to the manager
    assigned = dm.assign(ns, func_def)
    # The returned definition should be the one stored in the manager
    assert assigned is dm.get(ns)
    # A return pointer definition must be created
    return_ns = utils.join_ns(ns, utils.constants.RETURN_NAME)
    assert return_ns in dm.get_defs()
    return_def = dm.get(return_ns)
    # The return definition should be of type NAME_DEF
    assert return_def.get_type() == utils.constants.NAME_DEF
    # Its name pointer should contain the function's return name
    expected_return_name = utils.join_ns(ns, utils.constants.RETURN_NAME)
    assert expected_return_name in return_def.get_name_pointer().get()
    # The original definition's name pointer should still contain the added name
    assert 'pkg.mod.other' in assigned.get_name_pointer().get()
