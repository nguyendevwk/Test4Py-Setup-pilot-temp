import datetime
import pytest
from decimal import Decimal

from pypara.dcc import dcc, DCCRegistry, DCC, ZERO

# --------------------------------------------------------------------------- #
# Test 1: Registration conflict raises TypeError
# --------------------------------------------------------------------------- #
def test_dcc_registration_conflict():
    # Define a simple day count function
    def simple_func(start, asof, end, freq=None):
        return Decimal(1)

    # Register a convention with a main name
    @dcc("TestConvention")
    def func1(start, asof, end, freq=None):
        return simple_func(start, asof, end, freq)

    # Attempt to register another convention with the same main name
    with pytest.raises(TypeError, match="already registered"):
        @dcc("TestConvention")
        def func2(start, asof, end, freq=None):
            return simple_func(start, asof, end, freq)

    # Attempt to register a convention with an alternative name that conflicts
    @dcc("UniqueConvention", altnames={"ConflictAlt"})
    def func3(start, asof, end, freq=None):
        return simple_func(start, asof, end, freq)

    with pytest.raises(TypeError, match="already registered"):
        @dcc("AnotherConvention", altnames={"ConflictAlt"})
        def func4(start, asof, end, freq=None):
            return simple_func(start, asof, end, freq)

# --------------------------------------------------------------------------- #
# Test 2: find method respects stripping and uppercasing
# --------------------------------------------------------------------------- #
def test_dcc_registry_find_stripping_and_uppercasing():
    # Register a convention with mixed case and spaces
    @dcc("  MixedCase  ")
    def mixed_func(start, asof, end, freq=None):
        return Decimal(0)

    # Should find by exact name
    found_exact = DCCRegistry.find("  MixedCase  ")
    assert found_exact is not None
    assert found_exact.name == "  MixedCase  "

    # Should find by stripped and uppercased name
    found_stripped = DCCRegistry.find("mixedcase")
    assert found_stripped is not None
    assert found_stripped.name == "  MixedCase  "

    # Should not find a non-existent name
    assert DCCRegistry.find("NonExistent") is None

# --------------------------------------------------------------------------- #
# Test 3: calculate_fraction returns ZERO when dates are out of order
# --------------------------------------------------------------------------- #
def test_dcc_calculate_fraction_boundary():
    # Register a convention that simply returns the difference in days
    @dcc("DiffDays")
    def diff_func(start, asof, end, freq=None):
        return Decimal((end - start).days)

    dcc_obj = DCCRegistry.find("DiffDays")
    assert dcc_obj is not None

    start = datetime.date(2023, 1, 1)
    end = datetime.date(2023, 1, 10)
    asof_in_range = datetime.date(2023, 1, 5)
    asof_before = datetime.date(2022, 12, 31)
    asof_after = datetime.date(2023, 1, 11)

    # Normal case: asof within range
    assert dcc_obj.calculate_fraction(start, asof_in_range, end) == Decimal(9)

    # Boundary case: asof before start
    assert dcc_obj.calculate_fraction(start, asof_before, end) == ZERO

    # Boundary case: asof after end
    assert dcc_obj.calculate_fraction(start, asof_after, end) == ZERO
