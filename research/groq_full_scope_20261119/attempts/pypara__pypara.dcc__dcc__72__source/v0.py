import pytest
from pypara.dcc import dcc, DCCRegistry, DCC
from pypara.currencies import Currency
from pypara.monetary import Money
from pypara.commons.zeitgeist import Date

# Helper to clear registry between tests
@pytest.fixture(autouse=True)
def clear_registry():
    DCCRegistry._registry.clear()
    yield
    DCCRegistry._registry.clear()


def test_register_basic():
    """Register a simple DCC and verify it is stored in the registry."""
    @dcc("simple")
    def simple_dcc(start: Date, end: Date) -> float:
        return (end - start).days

    # The function should have a __dcc attribute
    assert hasattr(simple_dcc, "__dcc")
    dcc_obj: DCC = getattr(simple_dcc, "__dcc")

    # Registry should contain the DCC under its name
    assert "simple" in DCCRegistry._registry
    assert DCCRegistry._registry["simple"] is dcc_obj

    # The DCC instance should expose the original function
    assert dcc_obj.func is simple_dcc

    # Test the calculation works as expected
    start = Date(2023, 1, 1)
    end = Date(2023, 1, 11)
    assert simple_dcc(start, end) == 10.0


def test_register_with_altnames_and_ccys():
    """Register a DCC with alternative names and currencies and verify registry entries."""
    usd = Currency("USD")
    eur = Currency("EUR")

    @dcc("custom", altnames={"alt1", "alt2"}, ccys={usd, eur})
    def custom_dcc(start: Date, end: Date) -> float:
        return (end - start).days / 2

    dcc_obj: DCC = getattr(custom_dcc, "__dcc")

    # Main name registration
    assert "custom" in DCCRegistry._registry
    assert DCCRegistry._registry["custom"] is dcc_obj

    # Alternative names should also point to the same DCC
    for alt in {"alt1", "alt2"}:
        assert alt in DCCRegistry._registry
        assert DCCRegistry._registry[alt] is dcc_obj

    # Currency set should match
    assert dcc_obj.ccys == {usd, eur}

    # Verify calculation
    start = Date(2023, 1, 1)
    end = Date(2023, 1, 5)
    assert custom_dcc(start, end) == 2.0


def test_duplicate_registration_raises():
    """Attempting to register a DCC with a name already in use should raise an exception."""
    @dcc("dup")
    def first_dcc(start: Date, end: Date) -> float:
        return (end - start).days

    # Registering another function with the same name should raise ValueError
    with pytest.raises(ValueError):
        @dcc("dup")
        def second_dcc(start: Date, end: Date) -> float:
            return (end - start).days * 2
