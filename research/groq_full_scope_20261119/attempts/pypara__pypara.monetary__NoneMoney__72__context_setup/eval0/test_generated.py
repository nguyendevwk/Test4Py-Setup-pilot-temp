import pytest
from decimal import Decimal
from pypara.monetary import NoneMoney, NoPrice
from pypara.currencies import Currency
from pypara.commons.zeitgeist import Date

# Helper dummy currency and date for tests
class DummyCurrency(Currency):
    def __init__(self, code: str):
        self.code = code

    def __repr__(self):
        return f"DummyCurrency({self.code!r})"

class DummyDate(Date):
    def __init__(self, year: int, month: int, day: int):
        super().__init__(year, month, day)

def test_none_money_comparisons_and_definedness():
    nm = NoneMoney()
    # defined/undefined flags
    assert not nm.defined
    assert nm.undefined
    # boolean conversion
    assert bool(nm) is False
    # equality only with same class
    assert nm == NoneMoney()
    assert nm != NoneMoney()  # same class but different instance still equal by class check
    # comparison with defined money (using a dummy Money subclass)
    class DummyMoney:
        @property
        def defined(self):
            return True
    dm = DummyMoney()
    assert nm < dm  # lt returns other.defined
    assert nm <= dm  # lte always True
    assert nm > dm is False
    assert nm >= dm  # gte returns other.undefined which is False, so False

def test_none_money_arithmetic_and_or_else():
    nm = NoneMoney()
    # Arithmetic with another NoneMoney
    assert nm + nm is nm
    assert nm - nm is nm
    # Arithmetic with a defined Money instance (dummy)
    class DummyMoney:
        def __init__(self, qty):
            self.qty = qty
        def __repr__(self):
            return f"DummyMoney({self.qty})"
    dm = DummyMoney(Decimal('10'))
    # add returns other
    assert nm + dm is dm
    # subtract returns -other
    assert nm - dm == -dm
    # scalar operations return self
    assert nm.multiply(2) is nm
    assert nm.divide(2) is nm
    # or_else executes fallback
    fallback = DummyMoney(Decimal('5'))
    assert nm.or_else(lambda: fallback) is fallback

def test_none_money_conversion_and_price_property():
    nm = NoneMoney()
    # conversion returns self regardless of target
    dummy_cur = DummyCurrency("USD")
    assert nm.convert(dummy_cur) is nm
    # price property returns NoPrice instance
    assert isinstance(nm.price, NoPrice)
    # NoPrice behaves similarly to NoneMoney
    assert not nm.price.defined
    assert nm.price.undefined
    assert nm.price == NoPrice()
    # price's as_float raises TypeError
    with pytest.raises(TypeError):
        _ = nm.price.as_float()
