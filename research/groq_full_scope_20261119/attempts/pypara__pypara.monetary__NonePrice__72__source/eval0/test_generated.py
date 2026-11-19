import pytest
from decimal import Decimal
from pypara.monetary import NonePrice, NoMoney
from pypara.currencies import Currency
from pypara.commons.zeitgeist import Date

def test_noneprice_comparisons_and_arithmetic():
    np = NonePrice()
    # Comparisons
    assert np.defined is False
    assert np.undefined is True
    assert np < NonePrice()  # other defined? False -> True
    assert np <= NonePrice()  # always True
    assert np > NonePrice()  # always False
    assert np >= NonePrice()  # other undefined? True
    # Arithmetic
    assert np + NonePrice() is NonePrice()
    assert np - NonePrice() == -NonePrice()
    assert np * 5 == np
    assert np / 2 == np
    assert np // 3 == np
    # Boolean and numeric conversions
    assert bool(np) is False
    with pytest.raises(TypeError):
        float(np)
    with pytest.raises(TypeError):
        int(np)

def test_noneprice_identity_and_or_else():
    np = NonePrice()
    # Identity operations
    assert np.abs() is np
    assert np.negative() is np
    assert np.positive() is np
    # or_else should call the supplier
    called = False
    def supplier():
        nonlocal called
        called = True
        return NonePrice()
    result = np.or_else(supplier)
    assert called is True
    assert result is np

def test_noneprice_with_optional_and_default_values():
    np = NonePrice()
    # Currency and quantity defaults
    default_ccy = Currency("USD")
    default_qty = Decimal("10.5")
    default_date = Date(2023, 1, 1)
    assert np.ccy_or(default_ccy) is default_ccy
    assert np.ccy_or_none() is None
    assert np.qty_or(default_qty) == default_qty
    assert np.qty_or_zero() == Decimal("0")
    assert np.qty_or_none() is None
    assert np.dov_or(default_date) == default_date
    assert np.dov_or_none() is None
    # Money property
    assert np.money is NoMoney
