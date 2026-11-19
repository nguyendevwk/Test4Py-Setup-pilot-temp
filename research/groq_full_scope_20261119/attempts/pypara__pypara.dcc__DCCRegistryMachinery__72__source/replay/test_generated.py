import pytest
from pypara.dcc import DCCRegistryMachinery

# Dummy DCC class for testing purposes
class DummyDCC:
    def __init__(self, name: str, altnames: list[str] | None = None):
        self.name = name
        self.altnames = altnames or []

def test_register_conflict_same_name():
    """Registering a DCC with an already used main name should raise TypeError."""
    registry = DCCRegistryMachinery()
    dcc1 = DummyDCC("ACT/ACT")
    dcc2 = DummyDCC("ACT/ACT")  # same main name
    registry.register(dcc1)
    with pytest.raises(TypeError, match="already registered"):
        registry.register(dcc2)

def test_register_conflict_altnames():
    """Registering a DCC whose alternative name conflicts with an existing main name should raise TypeError."""
    registry = DCCRegistryMachinery()
    dcc1 = DummyDCC("ACT/360")
    dcc2 = DummyDCC("ACT/365", altnames=["ACT/360"])  # alternative name conflicts with dcc1 main name
    registry.register(dcc1)
    with pytest.raises(TypeError, match="already registered"):
        registry.register(dcc2)

def test_find_strict_and_fallback():
    """The find method should first try the exact name, then strip and uppercase."""
    registry = DCCRegistryMachinery()
    dcc = DummyDCC("30/360 US")
    registry.register(dcc)

    # Exact match
    assert registry.find("30/360 US") is dcc

    # Case-insensitive and stripped match
    assert registry.find(" 30/360 us ") is dcc

    # Non-existent name returns None
    assert registry.find("NON/EXISTENT") is None
