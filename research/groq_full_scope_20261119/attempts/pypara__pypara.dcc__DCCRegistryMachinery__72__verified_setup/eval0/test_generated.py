import datetime
import pytest
from pypara.dcc import DCCRegistryMachinery

# Minimal stub for a DCC object used only for registration tests
class DummyDCC:
    def __init__(self, name: str, altnames: list[str] | None = None):
        self.name = name
        self.altnames = altnames or []

def test_register_and_find_basic():
    """Register a DCC and verify it can be found by main and alternative names."""
    registry = DCCRegistryMachinery()
    dcc = DummyDCC("Act/Act", ["ACT/ACT", "act/act"])
    registry.register(dcc)

    # Direct lookup by main name
    assert registry.find("Act/Act") is dcc

    # Lookup by alternative name (case-insensitive)
    assert registry.find("act/act") is dcc
    assert registry.find("ACT/ACT") is dcc

    # Lookup with whitespace and case changes
    assert registry.find("  act/act  ") is dcc

def test_register_conflict_on_main_and_altnames():
    """Registering a DCC with a duplicate main or alternative name raises TypeError."""
    registry = DCCRegistryMachinery()
    dcc1 = DummyDCC("Act/Act")
    dcc2 = DummyDCC("Act/Act")  # same main name
    dcc3 = DummyDCC("Act/Act", ["ACT/ACT"])  # duplicate alternative name

    registry.register(dcc1)

    # Duplicate main name
    with pytest.raises(TypeError, match="already registered"):
        registry.register(dcc2)

    # Duplicate alternative name
    with pytest.raises(TypeError, match="already registered"):
        registry.register(dcc3)

def test_registry_table_and_properties():
    """Verify that registry.table contains all entries and registry.registry returns list."""
    registry = DCCRegistryMachinery()
    dcc_main = DummyDCC("Act/Act")
    dcc_alt = DummyDCC("Act/Act", ["ACT/ACT"])
    registry.register(dcc_main)
    registry.register(dcc_alt)

    # registry.table should contain both main and alternative entries
    table = registry.table
    assert "Act/Act" in table
    assert "ACT/ACT" in table
    assert table["Act/Act"] is dcc_main
    assert table["ACT/ACT"] is dcc_alt

    # registry.registry should list only main entries
    registry_list = registry.registry
    assert dcc_main in registry_list
    assert dcc_alt not in registry_list
    assert len(registry_list) == 2
