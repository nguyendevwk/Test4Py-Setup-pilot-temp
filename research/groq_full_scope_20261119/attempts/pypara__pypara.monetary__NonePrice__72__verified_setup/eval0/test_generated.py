import pytest
from decimal import Decimal
from pypara.monetary import NonePrice, NoMoney
from pypara.currencies import Currency
from pypara.commons.zeitgeist import Date

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
    assert np < NonePrice()  # other defined -> False, but defined is False so True
    assert np <= NonePrice()  # always True
    assert np > NonePrice()  # always False
    assert np >= NonePrice()  # other undefined -> True

def test_noneprice_arithmetic_and_methods():
    np = NonePrice()
    # arithmetic with another NonePrice returns the other
    other = NonePrice()
    assert np + other is other
    assert np - other == -other
    # scalar operations return self
    assert np * 5 == np
    assert np / 2 == np
    assert np // 3 == np
    # abs, positive, negative are identity
    assert abs(np) is np
    assert +np is np
    assert -np == np
    # conversion and quantity access return defaults
    assert np.qty_or(Decimal('10')) == Decimal('10')
    assert np.qty_or_zero() == Decimal('0')
    assert np.ccy_or(Currency('USD')) == Currency('USD')
    assert np.dov_or(Date(2020, 1, 1)) == Date(2020, 1, 1)

def test_noneprice_or_else_and_fmap():
    np = NonePrice()
    # or_else should invoke the supplier
    called = False
    def supplier():
        nonlocal called
        called = True
        return NonePrice()
    result = np.or_else(supplier)
    assert called
    assert result is np  # supplier returns a new NonePrice, but or_else returns that
    # fmap returns self regardless of function
    def dummy_func(x):
        return NoMoney
    assert np.fmap(dummy_func) is np
