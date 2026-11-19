import pytest
from decimal import Decimal
from pypara.monetary import NonePrice, NoMoney
from pypara.currencies import Currency
from pypara.commons.zeitgeist import Date

def test_noneprice_properties_and_equality():
    np = NonePrice()
    # defined/undefined flags
    assert not np.defined
    assert np.undefined
    # boolean conversion
    assert bool(np) is False
    # equality only with same class
    assert np == NonePrice()
    assert np != 42
    # quantity and currency defaults
    assert np.qty_or(Decimal("123.45")) == Decimal("123.45")
    assert np.qty_or_zero() == Decimal("0")
    assert np.ccy_or(Currency("USD")) == Currency("USD")
    # conversion returns self
    assert np.convert(Currency("EUR")) is np

def test_noneprice_arithmetic_and_comparisons():
    np = NonePrice()
    # arithmetic with another NonePrice
    assert np + np is np
    assert np - np is np
    # arithmetic with Money returns NoMoney
    assert np.times(Decimal("2")) is NoMoney
    # scalar operations return self
    assert np.multiply(Decimal("3")) is np
    assert np.scalar_add(Decimal("5")) is np
    # comparisons
    assert np < NonePrice() is True
    assert np <= NonePrice() is True
    assert np > NonePrice() is False
    assert np >= NonePrice() is True

def test_noneprice_error_and_or_else():
    np = NonePrice()
    # as_float and as_integer raise TypeError
    with pytest.raises(TypeError):
        float(np)
    with pytest.raises(TypeError):
        int(np)
    # or_else executes fallback
    fallback = NonePrice()
    assert np.or_else(lambda: fallback) is fallback
    # fmap and dimap return self or fallback
    assert np.fmap(lambda x: x) is np
    assert np.dimap(lambda x: x, lambda: "fallback") == "fallback"
