import pytest
from decimal import Decimal
from pypara.monetary import NonePrice, NoMoney
from pypara.currencies import Currency
from pypara.commons.zeitgeist import Date

def test_noneprice_properties_and_methods():
    np = NonePrice()
    # defined/undefined flags
    assert not np.defined
    assert np.undefined
    # boolean conversion
    assert bool(np) is False
    # equality only with same class
    assert np == NonePrice()
    assert np != NonePrice()  # same instance but __eq__ uses class, so True
    # numeric conversions raise TypeError
    with pytest.raises(TypeError):
        float(np)
    with pytest.raises(TypeError):
        int(np)
    # arithmetic returns self or other appropriately
    assert np + np is np
    assert np - np == -np
    assert np * 5 == np
    assert np / 2 == np
    assert np // 3 == np
    # abs, positive, negative are identity
    assert abs(np) is np
    assert +np is np
    assert -np == np
    # round returns self
    assert np.round(2) is np
    # scalar_add returns self
    assert np.scalar_add(Decimal('10')) is np
    # times returns NoMoney
    assert np.times(Decimal('2')) is NoMoney

def test_noneprice_comparisons_and_or_else():
    np = NonePrice()
    defined_price = pytest.Mock(defined=True, undefined=False)
    undefined_price = pytest.Mock(defined=False, undefined=True)
    # lt: returns other.defined
    assert np.lt(defined_price) is True
    assert np.lt(undefined_price) is False
    # lte: always True
    assert np.lte(defined_price) is True
    assert np.lte(undefined_price) is True
    # gt: always False
    assert np.gt(defined_price) is False
    assert np.gt(undefined_price) is False
    # gte: returns other.undefined
    assert np.gte(defined_price) is False
    assert np.gte(undefined_price) is True
    # or_else executes callable
    called = False
    def factory():
        nonlocal called
        called = True
        return NonePrice()
    result = np.or_else(factory)
    assert called is True
    assert result is np

def test_noneprice_with_currency_and_quantity():
    np = NonePrice()
    usd = Currency('USD')
    qty = Decimal('100')
    date = Date(2023, 1, 1)
    # with_ccy, with_qty, with_dov return self
    assert np.with_ccy(usd) is np
    assert np.with_qty(qty) is np
    assert np.with_dov(date) is np
    # ccy_or returns default
    assert np.ccy_or(usd) is usd
    assert np.ccy_or_none() is None
    # qty_or returns default
    assert np.qty_or(qty) == qty
    assert np.qty_or_zero() == Decimal('0')
    assert np.qty_or_none() is None
    # dov_or returns default
    assert np.dov_or(date) == date
    assert np.dov_or_none() is None
