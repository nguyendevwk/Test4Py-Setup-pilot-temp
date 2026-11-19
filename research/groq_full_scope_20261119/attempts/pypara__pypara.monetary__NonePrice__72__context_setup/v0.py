import pytest
from decimal import Decimal
from pypara.monetary import NonePrice, NoMoney, Currency, Date

# Helper dummy objects for comparison
class DummyPrice:
    def __init__(self, defined=True):
        self.defined = defined
        self.undefined = not defined

def test_noneprice_defined_and_boolean():
    np = NonePrice()
    # defined/undefined flags
    assert not np.defined
    assert np.undefined
    # boolean conversion
    assert bool(np) is False
    # equality only with other NonePrice
    assert np == NonePrice()
    assert np != DummyPrice()
    # arithmetic: adding any price returns the other
    dummy = DummyPrice()
    assert np + dummy is dummy
    assert dummy + np is dummy

def test_noneprice_comparisons_and_or_else():
    np = NonePrice()
    defined_price = DummyPrice(defined=True)
    undefined_price = DummyPrice(defined=False)

    # lt: returns True only if other is defined
    assert np < defined_price is True
    assert np < undefined_price is False

    # lte: always True
    assert np <= defined_price is True
    assert np <= undefined_price is True

    # gt: always False
    assert np > defined_price is False
    assert np > undefined_price is False

    # gte: True if other is undefined
    assert np >= defined_price is False
    assert np >= undefined_price is True

    # or_else: should call the supplier
    called = False
    def supplier():
        nonlocal called
        called = True
        return DummyPrice()
    result = np.or_else(supplier)
    assert called is True
    assert isinstance(result, DummyPrice)

def test_noneprice_arithmetic_and_conversion():
    np = NonePrice()
    # subtract: returns negative of other
    dummy = DummyPrice()
    assert np - dummy is dummy  # dummy is not negated because DummyPrice has no __neg__
    # multiply/divide: return self
    assert np * 5 is np
    assert np / 2 is np
    # convert: returns self
    assert np.convert(Currency("USD")) is np
    # money property returns NoMoney
    assert np.money is NoMoney
    # qty_or and dov_or return defaults
    assert np.qty_or(Decimal("10")) == Decimal("10")
    assert np.dov_or(Date(2023, 1, 1)) == Date(2023, 1, 1)
