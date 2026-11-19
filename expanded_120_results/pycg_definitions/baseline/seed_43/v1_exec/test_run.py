import pytest
from pycg.machinery.definitions import DefinitionManager, DefinitionError, Definition
from pycg.machinery import utils

def test_definition_manager_create_behavior():
    manager = DefinitionManager()

    # Invalid namespace: None or non-string
    with pytest.raises(DefinitionError):
        manager.create(None, utils.constants.FUN_DEF)
    with pytest.raises(DefinitionError):
        manager.create(123, utils.constants.FUN_DEF)

    # Invalid definition type
    with pytest.raises(DefinitionError):
        manager.create("valid.ns", "invalid_type")

    # Valid creation
    ns = "valid.ns"
    defi = manager.create(ns, utils.constants.FUN_DEF)
    assert isinstance(defi, Definition)
    assert manager.get(ns) is defi
    assert ns in manager.get_defs()

    # Duplicate namespace raises error
    with pytest.raises(DefinitionError) as excinfo:
        manager.create(ns, utils.constants.FUN_DEF)
    assert "Definition already exists" in str(excinfo.value)
