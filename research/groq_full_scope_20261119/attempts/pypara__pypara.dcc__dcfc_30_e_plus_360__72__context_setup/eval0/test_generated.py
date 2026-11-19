import datetime
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_30_e_plus_360


def test_normal_day_count_fraction():
    """Test a typical case where no date adjustments are required."""
    start = datetime.date(2007, 12, 28)
    asof = datetime.date(2008, 2, 28)
    end = asof
    result = dcfc_30_e_plus_360(start, asof, end)
    # Expected fraction from the docstring example
    assert result == Decimal('0.1666666666666666666666666667')


def test_boundary_day_adjustments():
    """Test the special handling of 31st days for start and asof dates."""
    # Start on 31st -> should be treated as 30th
    start = datetime.date(2007, 12, 31)
    # Asof on 31st -> should be incremented by one day
    asof = datetime.date(2008, 2, 28)  # 28th is not 31st, so no increment
    end = asof
    # Manually compute expected nod: (28-30)+30*(2-12)+360*(2008-2007) = -2+30*(-10)+360 = -2-300+360 = 58
    expected_fraction = Decimal(58) / Decimal(360)
    assert dcfc_30_e_plus_360(start, asof, end) == expected_fraction

    # Asof on 31st: increment by one day
    asof_31 = datetime.date(2008, 2, 31)
    # Since 2008 is leap year, Feb 31 is invalid; use March 1 instead to simulate increment
    asof_31 = datetime.date(2008, 3, 1)
    # Start remains 31st of December
    result = dcfc_30_e_plus_360(start, asof_31, asof_31)
    # Expected nod: (1-30)+30*(3-12)+360*(2008-2007) = -29+30*(-9)+360 = -29-270+360 = 61
    assert result == Decimal(61) / Decimal(360)


def test_negative_day_count_fraction():
    """Test that the function can produce a negative fraction when asof precedes start."""
    start = datetime.date(2008, 3, 1)
    asof = datetime.date(2008, 2, 28)
    end = asof
    # nod = (28-1)+30*(2-3)+360*(2008-2008) = 27+30*(-1)+0 = -3
    expected_fraction = Decimal(-3) / Decimal(360)
    assert dcfc_30_e_plus_360(start, asof, end) == expected_fraction
