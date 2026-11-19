import datetime
import pytest
from decimal import Decimal

from pypara.dcc import DCCRegistry, dcc, _last_payment_date, _next_payment_date, DCC, Money, Currencies


def test_register_duplicate_raises():
    """Registering a DCC with an already used name or alternative name raises TypeError."""
    # Define a simple day count fraction calculator
    @dcc("Test/Act", altnames={"Test/Act Alternative"})
    def test_calc(start, asof, end, freq=None):
        return Decimal(1)

    # Attempt to register another DCC with the same main name
    with pytest.raises(TypeError, match="already registered"):
        @dcc("Test/Act")
        def dup_calc(start, asof, end, freq=None):
            return Decimal(1)

    # Attempt to register another DCC with the same alternative name
    with pytest.raises(TypeError, match="already registered"):
        @dcc("Another/Act", altnames={"Test/Act Alternative"})
        def dup_alt_calc(start, asof, end, freq=None):
            return Decimal(1)


def test_find_case_insensitive_and_stripped():
    """DCCRegistry.find should locate conventions regardless of case and surrounding whitespace."""
    # Register a convention with mixed case and spaces
    @dcc("  Mixed/Case  ")
    def mixed_calc(start, asof, end, freq=None):
        return Decimal(1)

    # Direct lookup with exact name
    assert DCCRegistry.find("  Mixed/Case  ") is not None

    # Lookup with different case
    assert DCCRegistry.find("mixed/case") is not None

    # Lookup with stripped and uppercased name
    assert DCCRegistry.find("MIXED/CASE") is not None

    # Lookup with leading/trailing whitespace
    assert DCCRegistry.find("  MIXED/CASE  ") is not None

    # Ensure that a non-existent name returns None
    assert DCCRegistry.find("Nonexistent/Convention") is None


def test_last_payment_date_boundary_conditions():
    """_last_payment_date should correctly handle edge cases such as year boundaries and end-of-month."""
    # Case: asof before start month, should return previous year same month
    start = datetime.date(2020, 5, 15)
    asof = datetime.date(2021, 3, 10)  # earlier month than start
    result = _last_payment_date(start, asof, frequency=1)
    assert result == datetime.date(2020, 5, 15)

    # Case: asof exactly on a payment month but before eom, should return same month
    start = datetime.date(2020, 1, 31)
    asof = datetime.date(2020, 1, 30)
    result = _last_payment_date(start, asof, frequency=1)
    assert result == datetime.date(2020, 1, 31)

    # Case: asof on a payment month but after eom, should return previous month
    start = datetime.date(2020, 1, 31)
    asof = datetime.date(2020, 1, 31)
    result = _last_payment_date(start, asof, frequency=1)
    assert result == datetime.date(2020, 1, 31)

    # Case: frequency 2 (semiannual) with asof in middle of period
    start = datetime.date(2020, 1, 15)
    asof = datetime.date(2020, 6, 10)
    result = _last_payment_date(start, asof, frequency=2)
    assert result == datetime.date(2020, 1, 15)

    # Case: asof in next year, frequency 4 (quarterly)
    start = datetime.date(2020, 7, 7)
    asof = datetime.date(2021, 10, 6)
    result = _last_payment_date(start, asof, frequency=4)
    assert result == datetime.date(2021, 7, 7)
