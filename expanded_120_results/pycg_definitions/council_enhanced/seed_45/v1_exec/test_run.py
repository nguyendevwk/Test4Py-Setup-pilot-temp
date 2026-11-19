import pytest
from pycg.machinery.definitions import DefinitionManager, DefinitionError
import pycg.machinery.utils as utils

def test_assign_function_def_creates_return_pointer():
    dm = DefinitionManager()
    ns = 'pkg.mod.func'
    # create function definition
    func_def = dm.create(ns, utils.constants.FUN_DEF)
    # assign the same definition
    returned_def = dm.assign(ns, func_def)
    # returned_def should be the function definition
    assert returned_def is dm.get(ns)
    assert returned_def.get_type() == utils.constants.FUN_DEF
    # return namespace
    return_ns = utils.join_ns(ns, utils.constants.RETURN_NAME)
    return_def = dm.get(return_ns)
    assert return_def is not None
    assert return_def.get_type() == utils.constants.NAME_DEF
    # the return definition's name pointer should contain the function's return name
    expected_return_name = utils.join_ns(ns, utils.constants.RETURN_NAME)
    assert expected_return_name in return_def.get_name_pointer().get()
