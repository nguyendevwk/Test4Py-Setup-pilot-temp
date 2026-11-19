import datetime
import decimal
import pytest
from pypara.dcc import dcfc_30_360_german

def test_normal_example():
    """Verify the function against the documented example."""
    start = datetime.date(2007, 12, 28)
    asof = datetime.date(2008, 2, 28)
    end = asof
    result = dcfc_30_360_german(start, asof, end)
    assert isinstance(result, decimal.Decimal)
    assert round(result, 14) == decimal.Decimal('0.16666666666667')

def test_boundary_day_adjustments():
    """Check that days 31 and last day of February are adjusted to 30."""
    # Start on 31st January -> d1 should become 30
    start = datetime.date(2021, 1, 31)
    # asof on 28th February (not last day) -> d2 remains 28
    asof = datetime.date(2021, 2, 28)
    end = asof
    result = dcfc_30_360_german(start, asof, end)
    # Compute expected nod manually: (28-30)+30*(2-1)+360*(2021-2021)= -2+30=28
    expected = decimal.Decimal(28) / decimal.Decimal(360)
    assert result == expected

    # asof on 28th February but end != asof, d2 should become 30
    end = datetime.date(2021, 3, 1)
    result2 = dcfc_30_360_german(start, asof, end)
    # nod: (30-30)+30*(2-1)+360*0 = 30
    expected2 = decimal.Decimal(30) / decimal.Decimal(360)
    assert result2 == expected2

def test_invalid_input_type():
    """Passing an object without day/month/year attributes should raise AttributeError."""
    class BadDate:
        pass
    bad = BadDate()
    with pytest.raises(AttributeError):
        dcfc_30_360_german(bad, bad, bad)
