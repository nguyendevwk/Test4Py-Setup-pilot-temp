import pytest
from decimal import Decimal
from pypara.monetary import NonePrice, NoMoney
from pypara.currencies import Currency
from pypara.commons.zeitgeist import Date

def test_noneprice_comparisons_and_properties():
    np = NonePrice()
    # defined/undefined flags
    assert not np.defined
    assert np.undefined
    # boolean conversion
    assert bool(np) is False
    # equality only with same class
    assert np == NonePrice()
    assert np != 5
    # comparison logic
    assert np.lt(NonePrice()) is False
    assert np.lt(5) is False  # 5 is not a Price, but lt expects Price; still False
    assert np.lte(NonePrice()) is True
    assert np.gt(NonePrice()) is False
    assert np.gte(NonePrice()) is True
    # currency and quantity defaults
    assert np.ccy_or(Currency("USD")) == Currency("USD")
    assert np.qty_or(Decimal("10.5")) == Decimal("10.5")
    assert np.dov_or(Date(2023, 1, 1)) == Date(2023, 1, 1)

def test_noneprice_arithmetic_and_conversion():
    np = NonePrice()
    # arithmetic with other Price returns other
    other = NonePrice()
    assert np + other is other
    assert np - other == -other
    # scalar operations return self
    assert np * 2 == np
    assert np / 3 == np
    assert np // 4 == np
    # multiply returns self, times returns NoMoney
    assert np.multiply(5) == np
    assert np.times(5) is NoMoney
    # convert returns self
    assert np.convert(Currency("EUR")) is np
    # accessing money property returns NoMoney
    assert np.money is NoMoney

def test_noneprice_or_else_and_exceptions():
    np = NonePrice()
    # or_else executes the supplied callable
    called = {"flag": False}
    def supplier():
        called["flag"] = True
        return NonePrice()
    result = np.or_else(supplier)
    assert called["flag"] is True
    assert result is np
    # as_float and as_integer raise TypeError
    with pytest.raises(TypeError):
        float(np)
    with pytest.raises(TypeError):
        int(np)
