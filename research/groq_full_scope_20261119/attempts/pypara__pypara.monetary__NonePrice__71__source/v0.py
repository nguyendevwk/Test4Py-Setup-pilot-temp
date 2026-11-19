import pytest
from decimal import Decimal
from pypara.monetary import NonePrice, NoMoney
from pypara.currencies import Currency
from pypara.commons.zeitgeist import Date

def test_defined_flags_and_boolean_behavior():
    np = NonePrice()
    # defined/undefined flags
    assert np.defined is False
    assert np.undefined is True
    # boolean conversion
    assert bool(np) is False
    # equality only with same class
    assert np == NonePrice()
    assert np != NonePrice()  # same instance but __eq__ uses class check, so still True
    # numeric conversions raise TypeError
    with pytest.raises(TypeError):
        float(np)
    with pytest.raises(TypeError):
        int(np)

def test_arithmetic_and_comparison():
    np = NonePrice()
    # addition returns other
    assert np + np == np
    # subtraction returns negative of other
    assert np - np == -np
    # multiplication returns self
    assert np * 5 == np
    # division returns self
    assert np / 2 == np
    # floor division returns self
    assert np // 3 == np
    # comparisons
    assert np < np  # other.defined is False
    assert np <= np  # always True
    assert np > np  # always False
    assert np >= np  # other.undefined is True

def test_or_else_and_conversion():
    np = NonePrice()
    # or_else executes provided callable
    called = False
    def factory():
        nonlocal called
        called = True
        return NonePrice()
    result = np.or_else(factory)
    assert called is True
    assert result is np
    # conversion returns self
    usd = Currency("USD")
    date = Date(2024, 1, 1)
    assert np.convert(usd, asof=date, strict=True) is np
    # currency and quantity defaults
    assert np.ccy_or(Currency("EUR")) == Currency("EUR")
    assert np.qty_or(Decimal("10.5")) == Decimal("10.5")
    assert np.qty_or_zero() == Decimal("0")
    # money property returns NoMoney
    assert np.money is NoMoney
