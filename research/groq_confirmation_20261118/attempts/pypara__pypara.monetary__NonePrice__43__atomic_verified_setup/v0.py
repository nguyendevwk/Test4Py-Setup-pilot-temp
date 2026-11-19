import pytest
from decimal import Decimal
from pypara.monetary import NonePrice, NoMoney
from pypara.currencies import Currency
from pypara.commons.zeitgeist import Date

def test_comparison_and_boolean_behavior():
    np = NonePrice()
    # Boolean conversion
    assert not np
    # Equality only with same class
    assert np == NonePrice()
    assert np != 5
    # Comparison semantics
    assert np.lt(NonePrice()) is True   # undefined < defined
    assert np.lte(NonePrice()) is True
    assert np.gt(NonePrice()) is False
    assert np.gte(NonePrice()) is True  # undefined >= undefined
    # With a defined price (mocked via subclass)
    class DummyPrice:
        defined = True
        undefined = False
    dummy = DummyPrice()
    assert np.lt(dummy) is True
    assert np.gte(dummy) is False

def test_arithmetic_and_conversion_behavior():
    np = NonePrice()
    # Arithmetic with another price returns the other
    class DummyPrice:
        def __init__(self, val):
            self.val = val
        def __repr__(self):
            return f"DummyPrice({self.val})"
    d = DummyPrice(10)
    assert np + d is d
    assert np - d == -d
    # Scalar operations return self
    assert np * 2 is np
    assert np / 3 is np
    assert np // 4 is np
    # Conversion returns self
    usd = Currency("USD")
    assert np.convert(usd) is np
    # Money property returns NoMoney
    assert np.money is NoMoney

def test_or_else_and_mapping_behavior():
    np = NonePrice()
    # or_else executes the supplier
    called = False
    def supplier():
        nonlocal called
        called = True
        return NonePrice()
    result = np.or_else(supplier)
    assert called is True
    assert result is np
    # fmap returns self regardless of function
    def f(x):
        return 42
    assert np.fmap(f) is np
    # dimap executes the default supplier
    def g(x):
        return "ignored"
    def default():
        return "default"
    assert np.dimap(g, default) == "default"
    # ccy_or returns default currency
    eur = Currency("EUR")
    assert np.ccy_or(eur) is eur
    # qty_or returns default decimal
    default_qty = Decimal("123.45")
    assert np.qty_or(default_qty) == default_qty
    # dov_or returns default date
    default_date = Date(2023, 1, 1)
    assert np.dov_or(default_date) == default_date
