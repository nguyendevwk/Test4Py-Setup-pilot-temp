import datetime
import pytest
from decimal import Decimal

from pypara.dcc import dcc, DCCRegistry, DCC, ZERO


def dummy_calc(start, asof, end, freq=None):
    """Simple day count fraction: number of days divided by 365."""
    return Decimal((asof - start).days) / Decimal(365)


def test_register_and_find_unique_dcc(tmp_path):
    """Register a new DCC and verify it can be found by name and alternative names."""
    # Register a DCC with a unique name and an alternative name
    @dcc("Test/Act", altnames={"Test/Act Alternative"}, ccys=None)
    def calc(start, asof, end, freq=None):
        return dummy_calc(start, asof, end, freq)

    # The function should now have a __dcc attribute
    assert hasattr(calc, "__dcc")
    dcc_instance = calc.__dcc
    assert isinstance(dcc_instance, DCC)
    assert dcc_instance.name == "Test/Act"
    assert dcc_instance.altnames == {"Test/Act Alternative"}

    # The registry should contain the DCC under both names
    found_main = DCCRegistry.find("Test/Act")
    found_alt = DCCRegistry.find("Test/Act Alternative")
    assert found_main is dcc_instance
    assert found_alt is dcc_instance

    # Verify calculation works as expected
    start = datetime.date(2023, 1, 1)
    asof = datetime.date(2023, 7, 1)
    end = datetime.date(2024, 1, 1)
    expected = Decimal((asof - start).days) / Decimal(365)
    assert dcc_instance.calculate_fraction(start, asof, end) == expected


def test_register_duplicate_name_raises():
    """Attempting to register a DCC with a name that already exists should raise TypeError."""
    @dcc("Duplicate/Act")
    def first_calc(start, asof, end, freq=None):
        return dummy_calc(start, asof, end, freq)

    # Registering another DCC with the same main name should fail
    with pytest.raises(TypeError, match="already registered"):
        @dcc("Duplicate/Act")
        def second_calc(start, asof, end, freq=None):
            return dummy_calc(start, asof, end, freq)


def test_register_conflict_with_alternative_name_raises():
    """Registering a DCC whose alternative name conflicts with an existing main name should raise TypeError."""
    @dcc("Unique/Act")
    def unique_calc(start, asof, end, freq=None):
        return dummy_calc(start, asof, end, freq)

    # Attempt to register a new DCC where the alternative name clashes with an existing main name
    with pytest.raises(TypeError, match="already registered"):
        @dcc("Another/Act", altnames={"Unique/Act"})
        def conflict_calc(start, asof, end, freq=None):
            return dummy_calc(start, asof, end, freq)
