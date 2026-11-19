import pytest
from pycg.machinery.definitions import DefinitionManager, Definition, DefinitionError
from pycg.machinery import utils

def test_assign_function_def_creates_return_pointer_and_merges_pointers():
    dm = DefinitionManager()

    # Create a dummy function definition with a literal pointer
    func_ns = "pkg.mod.func"
    func_def = Definition(func_ns, utils.constants.FUN_DEF)
    func_def.get_lit_pointer().add("hello")

    # Assign the definition to the manager
    result = dm.assign(func_ns, func_def)

    # The returned object should be the stored definition
    assert result is dm.defs[func_ns]

    # The literal pointer should be merged into the stored definition
    assert result.get_lit_pointer().get() == {"hello"}

    # A return pointer definition should be created for a function definition
    return_ns = utils.join_ns(func_ns, utils.constants.RETURN_NAME)
    assert return_ns in dm.defs
    return_def = dm.defs[return_ns]
    # The return definition should be of type NAME_DEF
    assert return_def.get_type() == utils.constants.NAME_DEF
    # Its name pointer should contain the return namespace itself
    assert return_def.get_name_pointer().get() == {return_ns}

    # Assigning a non-function definition should not create a return pointer
    non_func_ns = "pkg.mod.var"
    non_func_def = Definition(non_func_ns, utils.constants.NAME_DEF)
    dm.assign(non_func_ns, non_func_def)
    assert utils.join_ns(non_func_ns, utils.constants.RETURN_NAME) not in dm.defs
