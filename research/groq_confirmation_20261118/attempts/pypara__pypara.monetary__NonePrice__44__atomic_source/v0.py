import pytest
from decimal import Decimal
from pypara.monetary import NonePrice
from pypara.currencies import Currency
from pypara.zeitgeist import Date

def test_noneprice_properties_and_comparisons():
    np = NonePrice()
    # defined/undefined flags
    assert not np.defined
    assert np.undefined
    # boolean conversion
    assert bool(np) is False
    # equality only with same class
    assert np == NonePrice()
    assert np != 42
    # comparison semantics
    assert np < NonePrice()  # other defined? no, so False
    assert np <= NonePrice()  # always True
    assert np > NonePrice()  # always False
    assert np >= NonePrice()  # other undefined? True

def test_noneprice_arithmetic_and_conversion():
    np = NonePrice()
    # arithmetic with other NonePrice returns other
    other = NonePrice()
    assert np + other is other
    assert np - other == -other
    # scalar operations return self
    assert np * 5 == np
    assert np / 2 == np
    assert np // 3 == np
    # conversion and currency methods return self or defaults
    assert np.convert(Currency("USD")) is np
    assert np.with_ccy(Currency("EUR")) is np
    assert np.with_qty(Decimal("10")) is np
    assert np.with_dov(Date.today()) is np

def test_noneprice_exceptions_and_fallbacks():
    np = NonePrice()
    # as_float and as_integer raise TypeError
    with pytest.raises(TypeError):
        float(np)
    with pytest.raises(TypeError):
        int(np)
    # or_else executes fallback
    fallback = NonePrice()
    assert np.or_else(lambda: fallback) is fallback
    # qty_or_else executes fallback
    assert np.qty_or_else(lambda: Decimal("7.5")) == Decimal("7.5")
    # ccy_or returns default
    assert np.ccy_or(Currency("GBP")) == Currency("GBP")
    # qty_or returns default
    assert np.qty_or(Decimal("3.14")) == Decimal("3.14")
    # dov_or returns default
    default_date = Date(2025, 1, 1)
    assert np.dov_or(default_date) == default_date
