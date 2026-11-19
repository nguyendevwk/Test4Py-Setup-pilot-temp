import pytest
from decimal import Decimal
from pypara.monetary import NoneMoney
from pypara.currencies import Currency
from pypara.commons.zeitgeist import Date

def test_none_money_comparisons_and_identity():
    nm = NoneMoney()
    # Identity and defined/undefined flags
    assert nm.defined is False
    assert nm.undefined is True
    # Equality only with other NoneMoney instances
    assert nm == NoneMoney()
    assert nm != 42
    # Comparison operators
    assert nm < NoneMoney()  # other defined? False -> True
    assert nm <= NoneMoney()  # always True
    assert nm > NoneMoney()  # always False
    assert nm >= NoneMoney()  # other.undefined? True -> True

def test_none_money_arithmetic_and_conversion():
    nm = NoneMoney()
    # Arithmetic with other Money returns the other operand
    other = NoneMoney()
    assert nm + other is other
    assert nm - other == -other
    # Scalar operations return self
    assert nm * 5 == nm
    assert nm / 3 == nm
    assert nm // 2 == nm
    # Conversion and currency/quantity methods return self or defaults
    assert nm.with_ccy(Currency("USD")) is nm
    assert nm.with_qty(Decimal("10")) is nm
    assert nm.with_dov(Date.today()) is nm
    assert nm.convert(Currency("EUR")) is nm
    # Price property returns NoPrice (placeholder)
    assert hasattr(nm, "price")

def test_none_money_error_and_or_else_behavior():
    nm = NoneMoney()
    # as_float and as_integer raise TypeError
    with pytest.raises(TypeError):
        nm.as_float()
    with pytest.raises(TypeError):
        nm.as_integer()
    # or_else executes the supplied callable
    def factory():
        return NoneMoney()
    assert nm.or_else(factory) is factory()
    # fmap and dimap return self or supplied default
    assert nm.fmap(lambda x: x) is nm
    assert nm.dimap(lambda x: x, lambda: "default") == "default"
    # qty_or_else and qty_map use the supplied fallback
    assert nm.qty_or_else(lambda: Decimal("5")) == Decimal("5")
    assert nm.qty_map(lambda x: x, lambda: Decimal("7")) == Decimal("7")
