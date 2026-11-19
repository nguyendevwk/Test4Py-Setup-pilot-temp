import pytest
from decimal import Decimal
from pypara.monetary import NonePrice, NoMoney
from pypara.currencies import Currency
from pypara.commons.zeitgeist import Date

def test_noneprice_properties_and_exceptions():
    np = NonePrice()
    # defined/undefined flags
    assert np.defined is False
    assert np.undefined is True
    # boolean conversion
    assert bool(np) is False
    # numeric conversions raise TypeError
    with pytest.raises(TypeError, match="Undefined monetary values do not have quantity information."):
        _ = np.as_float()
    with pytest.raises(TypeError, match="Undefined monetary values do not have quantity information."):
        _ = np.as_integer()
    # money property returns NoMoney
    assert np.money is NoMoney

def test_noneprice_arithmetic_and_identity():
    np = NonePrice()
    # addition returns other
    assert (np + np) is np
    assert (np + NoMoney) is NoMoney
    # subtraction returns negative of other
    assert (np - NoMoney) == -NoMoney
    # multiplication/division return self
    assert (np * 5) is np
    assert (np / 3) is np
    assert (np // 2) is np
    # scalar operations return self
    assert np.scalar_add(10) is np
    assert np.scalar_subtract(3) is np
    assert np.multiply(2) is np
    # times returns NoMoney
    assert np.times(2) is NoMoney

def test_noneprice_comparisons_and_fallbacks():
    np = NonePrice()
    # comparisons with defined price (NonePrice only)
    assert np.lt(np) is True
    assert np.lte(np) is True
    assert np.gt(np) is False
    assert np.gte(np) is True
    # or_else executes fallback
    fallback = NonePrice()
    assert np.or_else(lambda: fallback) is fallback
    # fmap returns self
    assert np.fmap(lambda x: x) is np
    # dimap returns fallback value
    assert np.dimap(lambda x: x, lambda: 42) == 42
    # ccy_or returns default
    default_ccy = Currency("USD")
    assert np.ccy_or(default_ccy) is default_ccy
    # qty_or returns default
    default_qty = Decimal("10")
    assert np.qty_or(default_qty) == default_qty
    # dov_or returns default
    default_date = Date(2023, 1, 1)
    assert np.dov_or(default_date) == default_date
