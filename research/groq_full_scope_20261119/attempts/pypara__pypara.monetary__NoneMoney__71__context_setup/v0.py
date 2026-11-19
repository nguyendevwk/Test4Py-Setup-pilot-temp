import pytest
from decimal import Decimal
from pypara.monetary import NoneMoney, NoPrice
from pypara.currencies import Currency
from pypara.commons.zeitgeist import Date

def test_none_money_properties_and_comparisons():
    nm = NoneMoney()
    # defined/undefined flags
    assert not nm.defined
    assert nm.undefined
    # boolean conversion
    assert bool(nm) is False
    # equality only with same class
    assert nm == NoneMoney()
    assert nm != NoPrice()
    # comparison semantics
    assert nm < NoneMoney()  # other undefined -> True
    assert nm <= NoneMoney()  # always True
    assert nm > NoneMoney()  # always False
    assert nm >= NoneMoney()  # other undefined -> True

def test_none_money_arithmetic_and_conversion():
    nm = NoneMoney()
    # arithmetic with another NoneMoney returns the other operand
    assert nm + NoneMoney() == NoneMoney()
    assert nm - NoneMoney() == NoneMoney()
    # scalar operations return self
    assert nm * 5 == nm
    assert nm / 2 == nm
    # conversion returns self
    dummy_ccy = Currency("USD")
    assert nm.convert(dummy_ccy) is nm
    # price property returns NoPrice
    assert isinstance(nm.price, NoPrice)

def test_none_money_error_and_or_else():
    nm = NoneMoney()
    # as_float and as_integer raise TypeError
    with pytest.raises(TypeError):
        float(nm)
    with pytest.raises(TypeError):
        int(nm)
    # or_else executes the supplied callable
    def fallback():
        return NoneMoney()
    assert nm.or_else(fallback) is fallback()
