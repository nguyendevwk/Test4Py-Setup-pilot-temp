import datetime
import pytest
from decimal import Decimal

from pypara.dcc import DCCRegistry, DCC, dcc, Money, Currencies


def test_register_conflict_raises_type_error(tmp_path):
    """Registering a DCC with a duplicate main name or alternative name raises TypeError."""
    # Define a simple DCC function
    @dcc("Test/Act")
    def _calc(start, asof, end, freq=None):
        return Decimal(1)

    # Attempt to register another DCC with the same main name
    with pytest.raises(TypeError, match="already registered"):
        @dcc("Test/Act")
        def _dup(start, asof, end, freq=None):
            return Decimal(2)

    # Attempt to register a DCC with an alternative name that conflicts
    @dcc("Unique/Act", altnames={"Conflict/Act"})
    def _unique(start, asof, end, freq=None):
        return Decimal(3)

    with pytest.raises(TypeError, match="already registered"):
        @dcc("Another/Act", altnames={"Conflict/Act"})
        def _conflict(start, asof, end, freq=None):
            return Decimal(4)


def test_find_case_insensitive_and_alternative_lookup():
    """DCCRegistry.find should locate conventions by stripped uppercase or alternative names."""
    # Register a convention with a mixed case name and alternative names
    @dcc("Mixed/Case", altnames={"Alt/Name", "Another/Alt"})
    def _calc(start, asof, end, freq=None):
        return Decimal(1)

    # Direct lookup with exact name
    assert DCCRegistry.find("Mixed/Case") is not None

    # Lookup with different case and surrounding whitespace
    assert DCCRegistry.find("  mixed/case  ") is not None

    # Lookup using an alternative name
    assert DCCRegistry.find("Alt/Name") is not None

    # Lookup using another alternative name
    assert DCCRegistry.find("Another/Alt") is not None

    # Ensure that a non‑existent name returns None
    assert DCCRegistry.find("Nonexistent/Name") is None


def test_interest_calculation_boundary_and_fraction():
    """Interest calculation should return zero when asof is outside the period."""
    # Create a principal Money instance
    principal = Money.of(Currencies["USD"], Decimal(1000), datetime.date.today())

    # Register a simple DCC that returns 0.5 for any valid period
    @dcc("Half/Year")
    def _half(start, asof, end, freq=None):
        return Decimal("0.5")

    dcc_obj = DCCRegistry.find("Half/Year")
    assert dcc_obj is not None

    # Case 1: asof within start and end -> interest should be 0.5 * rate * principal
    start = datetime.date(2023, 1, 1)
    end = datetime.date(2023, 12, 31)
    asof = datetime.date(2023, 6, 30)
    rate = Decimal("0.05")  # 5%
    interest = dcc_obj.interest(principal, rate, start, asof, end)
    assert interest.qty == Decimal("25.00")  # 1000 * 0.05 * 0.5

    # Case 2: asof before start -> fraction should be 0, interest 0
    asof_before = datetime.date(2022, 12, 31)
    interest_before = dcc_obj.interest(principal, rate, start, asof_before, end)
    assert interest_before.qty == Decimal("0.00")

    # Case 3: asof after end -> fraction should be 0, interest 0
    asof_after = datetime.date(2024, 1, 1)
    interest_after = dcc_obj.interest(principal, rate, start, asof_after, end)
    assert interest_after.qty == Decimal("0.00")
