import datetime
import pytest
from pypara.dcc import dcc
from pypara.dcc import DCCRegistry, DCC


def test_dcc_decorator_registers_and_attaches_function():
    # Define a simple day count fraction calculator
    @dcc("simple")
    def simple_dcf(start: datetime.date, end: datetime.date, ref: datetime.date, freq: float = None) -> float:
        return (end - start).days

    # The decorator should return the original function
    assert simple_dcf is not None
    assert callable(simple_dcf)

    # The function should have a __dcc attribute pointing to a DCC instance
    assert hasattr(simple_dcf, "__dcc")
    dcc_instance = getattr(simple_dcf, "__dcc")
    assert isinstance(dcc_instance, DCC)
    assert dcc_instance.name == "simple"
    assert dcc_instance.altnames == set()
    assert dcc_instance.ccys == set()

    # The DCC instance should be registered in the global registry
    registered = DCCRegistry.get("simple")
    assert registered is dcc_instance

    # Verify that the function works as expected
    start = datetime.date(2023, 1, 1)
    end = datetime.date(2023, 1, 11)
    ref = datetime.date(2023, 1, 1)
    assert simple_dcf(start, end, ref) == 10.0


def test_dcc_decorator_with_altnames_and_ccys():
    # Create dummy Currency objects for testing
    class DummyCurrency:
        def __init__(self, code):
            self.code = code

    usd = DummyCurrency("USD")
    eur = DummyCurrency("EUR")

    @dcc("alt_test", altnames={"alternative", "test"}, ccys={usd, eur})
    def alt_dcf(start: datetime.date, end: datetime.date, ref: datetime.date, freq: float = None) -> float:
        return (end - start).days / 30.0

    dcc_inst = getattr(alt_dcf, "__dcc")
    assert isinstance(dcc_inst, DCC)
    assert dcc_inst.name == "alt_test"
    assert dcc_inst.altnames == {"alternative", "test"}
    assert dcc_inst.ccys == {usd, eur}

    # Ensure registry contains both the primary name and alternative names
    assert DCCRegistry.get("alt_test") is dcc_inst
    for alt in dcc_inst.altnames:
        assert DCCRegistry.get(alt) is dcc_inst

    # Test calculation
    start = datetime.date(2023, 1, 1)
    end = datetime.date(2023, 2, 1)
    ref = datetime.date(2023, 1, 1)
    assert alt_dcf(start, end, ref) == 1.0


def test_dcc_decorator_error_on_duplicate_name():
    # Register a DCC with a given name
    @dcc("duplicate")
    def first_dcf(start: datetime.date, end: datetime.date, ref: datetime.date, freq: float = None) -> float:
        return 0.0

    # Attempting to register another DCC with the same name should raise a ValueError
    with pytest.raises(ValueError):
        @dcc("duplicate")
        def second_dcf(start: datetime.date, end: datetime.date, ref: datetime.date, freq: float = None) -> float:
            return 1.0
