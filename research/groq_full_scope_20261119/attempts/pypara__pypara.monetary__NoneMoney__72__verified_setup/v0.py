import pytest
from decimal import Decimal
from pypara.monetary import NoneMoney
from pypara.currencies import Currency
from pypara.zeitgeist import Date

def test_comparison_and_boolean_behavior():
    nm = NoneMoney()
    # Boolean conversion
    assert not nm
    # Equality only with same class
    assert nm == NoneMoney()
    assert nm != object()
    # Ordering semantics
    assert nm < NoneMoney()  # other defined? False -> True
    assert nm <= NoneMoney()  # always True
    assert not (nm > NoneMoney())
    assert nm >= NoneMoney()  # other undefined? True

def test_arithmetic_and_conversion_operations():
    nm = NoneMoney()
    # Arithmetic with defined Money returns the other operand
    dummy = object()
    assert nm + dummy is dummy
    # Subtraction returns negative of other
    assert nm - dummy == -dummy
    # Scalar operations leave NoneMoney unchanged
    assert nm * 5 == nm
    assert nm / 2 == nm
    assert nm // 3 == nm
    # Conversion and currency/quantity methods return self or defaults
    assert nm.with_ccy(Currency("USD")) is nm
    assert nm.with_qty(Decimal("10")) is nm
    assert nm.with_dov(Date(2023, 1, 1)) is nm
    assert nm.convert(Currency("EUR")) is nm
    # Price property returns NoPrice (a sentinel)
    assert hasattr(nm, "price")

def test_error_and_or_else_behavior():
    nm = NoneMoney()
    # Operations that should raise TypeError
    with pytest.raises(TypeError):
        nm.as_float()
    with pytest.raises(TypeError):
        nm.as_integer()
    # or_else should execute the supplied callable
    called = {"value": None}
    def supplier():
        called["value"] = "supplied"
        return "result"
    assert nm.or_else(supplier) == "result"
    assert called["value"] == "supplied"
