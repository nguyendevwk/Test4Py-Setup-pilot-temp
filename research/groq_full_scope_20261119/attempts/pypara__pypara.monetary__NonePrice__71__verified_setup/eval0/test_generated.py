import pytest
from decimal import Decimal
from pypara.monetary import NonePrice, NoMoney
from pypara.currencies import Currency
from pypara.commons.zeitgeist import Date

def test_noneprice_basic_properties_and_comparisons():
    np = NonePrice()
    # defined/undefined flags
    assert not np.defined
    assert np.undefined
    # boolean conversion
    assert bool(np) is False
    # equality only with same class
    assert np == NonePrice()
    assert np != 42
    # comparison logic
    assert np < NonePrice()   # other defined? False -> True
    assert np <= NonePrice()  # always True
    assert np > NonePrice()   # always False
    assert np >= NonePrice()  # other undefined? True

def test_noneprice_arithmetic_and_or_else():
    np = NonePrice()
    other = NonePrice()
    # arithmetic with another NonePrice returns the other
    assert np + other is other
    assert np - other == -other
    # scalar operations return self
    assert np * 5 == np
    assert np / 2 == np
    assert np // 3 == np
    # or_else executes the supplied callable
    def factory():
        return NonePrice()
    assert np.or_else(factory) is factory()

def test_noneprice_conversion_and_exceptions():
    np = NonePrice()
    # conversion returns self
    assert np.convert(Currency("USD")) is np
    # accessing quantity or currency returns defaults
    assert np.qty_or(Decimal("10")) == Decimal("10")
    assert np.ccy_or(Currency("EUR")) == Currency("EUR")
    # as_float and as_integer raise TypeError
    with pytest.raises(TypeError):
        _ = np.as_float()
    with pytest.raises(TypeError):
        _ = np.as_integer()
    # money property returns NoMoney
    assert np.money is NoMoney
