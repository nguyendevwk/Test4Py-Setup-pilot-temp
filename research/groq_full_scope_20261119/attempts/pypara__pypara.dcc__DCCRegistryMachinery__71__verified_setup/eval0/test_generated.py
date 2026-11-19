import datetime
import pytest
from pypara.dcc import DCCRegistryMachinery, DCC

# Helper to create a minimal DCC instance
def make_dcc(name: str, altnames: list[str] | None = None) -> DCC:
    return DCC(name=name, altnames=altnames or [])

def test_register_and_find_basic():
    """Register a DCC and verify it can be found by main and alternative names."""
    registry = DCCRegistryMachinery()
    dcc = make_dcc("Act/Act", altnames=["ACT/ACT", "act/act"])
    registry.register(dcc)

    # Find by main name
    assert registry.find("Act/Act") is dcc
    # Find by alternative name
    assert registry.find("ACT/ACT") is dcc
    # Find by stripped and uppercased name
    assert registry.find(" act/act ") is dcc
    # Ensure registry table contains the entry under both main and alt keys
    table = registry.table
    assert "ACT/ACT" in table and table["ACT/ACT"] is dcc
    assert "ACT/ACT" in table and table["ACT/ACT"] is dcc
    # Unknown name returns None
    assert registry.find("Nonexistent") is None

def test_conflict_registration_raises():
    """Registering a DCC with a name that already exists should raise TypeError."""
    registry = DCCRegistryMachinery()
    dcc1 = make_dcc("Act/Act")
    dcc2 = make_dcc("Act/Act")
    registry.register(dcc1)
    with pytest.raises(TypeError, match="already registered"):
        registry.register(dcc2)

def test_alternative_name_conflict_raises():
    """Registering a DCC whose alternative name conflicts with an existing main name should raise."""
    registry = DCCRegistryMachinery()
    dcc1 = make_dcc("Act/Act")
    dcc2 = make_dcc("Other", altnames=["Act/Act"])
    registry.register(dcc1)
    with pytest.raises(TypeError, match="already registered"):
        registry.register(dcc2)
