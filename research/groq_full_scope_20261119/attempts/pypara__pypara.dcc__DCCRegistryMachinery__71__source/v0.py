import pytest
from pypara.dcc import DCCRegistryMachinery

# Simple stand‑in for the DCC type used by the registry
class DummyDCC:
    def __init__(self, name: str, altnames: list[str] | None = None):
        self.name = name
        self.altnames = altnames or []

def test_register_and_find_basic():
    """Register a convention and verify it can be found by name and alias."""
    registry = DCCRegistryMachinery()
    dcc = DummyDCC("Act/Act", altnames=["ACT/ACT", "act/act"])
    registry.register(dcc)

    # Direct lookup
    assert registry.find("Act/Act") is dcc
    # Alias lookup
    assert registry.find("ACT/ACT") is dcc
    # Case‑insensitive lookup
    assert registry.find("act/act") is dcc
    # Stripped and uppercased fallback
    assert registry.find("  act/act  ") is dcc

    # Registry table contains both main and alias entries
    table = registry.table
    assert "Act/Act" in table and table["Act/Act"] is dcc
    assert "ACT/ACT" in table and table["ACT/ACT"] is dcc
    assert "act/act" not in table  # aliases are stored in the alternate buffer only

def test_register_duplicate_name_raises():
    """Attempting to register a convention with a duplicate main name raises TypeError."""
    registry = DCCRegistryMachinery()
    dcc1 = DummyDCC("30/360")
    dcc2 = DummyDCC("30/360")
    registry.register(dcc1)
    with pytest.raises(TypeError, match="already registered"):
        registry.register(dcc2)

def test_register_conflict_with_alternate_name_raises():
    """Registering a convention whose alternate name conflicts with an existing main name raises TypeError."""
    registry = DCCRegistryMachinery()
    dcc1 = DummyDCC("Act/360")
    dcc2 = DummyDCC("Act/365", altnames=["Act/360"])
    registry.register(dcc1)
    with pytest.raises(TypeError, match="already registered"):
        registry.register(dcc2)
