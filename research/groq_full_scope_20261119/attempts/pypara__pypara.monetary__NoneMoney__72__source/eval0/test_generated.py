import pytest
from decimal import Decimal
from pypara.monetary import NoneMoney
from pypara.currencies import Currency
from pypara.commons.zeitgeist import Date

def test_none_money_comparisons():
    nm = NoneMoney()
    # defined/undefined flags
    assert not nm.defined
    assert nm.undefined
    # comparisons with defined money (using a dummy Money subclass)
    class DummyMoney:
        def __init__(self, defined=True):
            self._defined = defined
        @property
        def defined(self):
            return self._defined
        @property
        def undefined(self):
            return not self._defined
    defined = DummyMoney(True)
    undefined = DummyMoney(False)
    # lt: NoneMoney < defined is True, < undefined is False
    assert nm < defined
    assert not (nm < undefined)
    # lte: always True
    assert nm <= defined
    assert nm <= undefined
    # gt: always False
    assert not (nm > defined)
    assert not (nm > undefined)
    # gte: True if other is undefined
    assert nm >= undefined
    assert not (nm >= defined)

def test_none_money_or_else_and_mapping():
    nm = NoneMoney()
    # or_else should call the provided function
    called = False
    def factory():
        nonlocal called
        called = True
        return NoneMoney()
    result = nm.or_else(factory)
    assert called
    assert isinstance(result, NoneMoney)
    # fmap should return self unchanged
    assert nm.fmap(lambda x: x) is nm
    # dimap should call the second function
    called_e = False
    def e_func():
        nonlocal called_e
        called_e = True
        return 42
    assert nm.dimap(lambda x: x, e_func) == 42
    assert called_e

def test_none_money_quantity_and_currency_defaults():
    nm = NoneMoney()
    # qty_or returns default
    default_qty = Decimal("123.45")
    assert nm.qty_or(default_qty) == default_qty
    # qty_or_zero returns ZERO
    from pypara.commons.numbers import ZERO
    assert nm.qty_or_zero() == ZERO
    # qty_or_none returns None
    assert nm.qty_or_none() is None
    # qty_or_else calls provided function
    called = False
    def alt():
        nonlocal called
        called = True
        return Decimal("9.99")
    assert nm.qty_or_else(alt) == Decimal("9.99")
    assert called
    # ccy_or returns default currency
    default_ccy = Currency("USD")
    assert nm.ccy_or(default_ccy) == default_ccy
    # ccy_or_none returns None
    assert nm.ccy_or_none() is None
    # dov_or returns default date
    default_date = Date(2023, 1, 1)
    assert nm.dov_or(default_date) == default_date
    # dov_or_none returns None
    assert nm.dov_or_none() is None
