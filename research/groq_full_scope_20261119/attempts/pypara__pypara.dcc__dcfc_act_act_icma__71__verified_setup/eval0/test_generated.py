import datetime
import decimal
import pytest
from pypara.dcc import dcfc_act_act_icma

def test_example_fraction():
    """Verify the example from the docstring."""
    start = datetime.date(2019, 3, 2)
    asof  = datetime.date(2019, 9, 10)
    end   = datetime.date(2020, 3, 2)
    result = dcfc_act_act_icma(start=start, asof=asof, end=end)
    assert isinstance(result, decimal.Decimal)
    assert result == decimal.Decimal('0.5245901639')

def test_full_period_fraction():
    """When asof equals end, the fraction should be 1."""
    start = datetime.date(2021, 1, 1)
    end   = datetime.date(2022, 1, 1)
    result = dcfc_act_act_icma(start=start, asof=end, end=end)
    assert result == decimal.Decimal('1')

def test_invalid_frequency_raises():
    """Providing a non‑positive frequency should raise a ValueError."""
    start = datetime.date(2020, 1, 1)
    asof  = datetime.date(2020, 6, 1)
    end   = datetime.date(2021, 1, 1)
    with pytest.raises(ValueError):
        dcfc_act_act_icma(start=start, asof=asof, end=end, freq=decimal.Decimal('0'))
