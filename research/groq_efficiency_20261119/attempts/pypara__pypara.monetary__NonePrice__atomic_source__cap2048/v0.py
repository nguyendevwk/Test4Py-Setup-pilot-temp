import pytest
from decimal import Decimal
from pypara.monetary import NonePrice, NoMoney
from pypara.currencies import Currency
from pypara.commons.zeitgeist import Date

def test_noneprice_comparisons_and_arithmetic(tmp_path):
    np = NonePrice()
    # defined/undefined flags
    assert not np.defined
    assert np.undefined
    # boolean conversion
    assert bool(np) is False
    # equality only with same class
    assert np == NonePrice()
    assert np != 42
    # comparison operators
    assert np < NonePrice()          # other defined? False -> True
    assert np <= NonePrice()         # always True
    assert np > NonePrice()          # always False
    assert np >= NonePrice()         # other undefined? True
    # arithmetic with another NonePrice
    assert np + NonePrice() is NonePrice()
    assert np - NonePrice() is NonePrice()
    assert np * 5 == np
    assert np / 3 == np
    assert np // 2 == np
    # scalar operations
    assert np.scalar_add(10) is np
    assert np.scalar_subtract(3) is np
    assert np.multiply(2) is np
    # conversion returns self
    assert np.convert(Currency("USD")) is np
    # money property returns NoMoney
    assert np.money is NoMoney

def test_noneprice_or_else_and_mappings(tmp_path):
    np = NonePrice()
    # or_else should call the supplier
    called = {"flag": False}
    def supplier():
        called["flag"] = True
        return NonePrice()
    result = np.or_else(supplier)
    assert called["flag"] is True
    assert result is np
    # fmap returns self
    assert np.fmap(lambda x: x) is np
    # dimap returns e()
    called_e = {"value": None}
    def e():
        called_e["value"] = 123
        return 123
    assert np.dimap(lambda x: x, e) == 123
    assert called_e["value"] == 123

def test_noneprice_exceptions_and_defaults(tmp_path):
    np = NonePrice()
    # as_float and as_integer raise TypeError
    with pytest.raises(TypeError, match="Undefined monetary values do not have quantity information."):
        float(np)
    with pytest.raises(TypeError, match="Undefined monetary values do not have quantity information."):
        int(np)
    # default getters
    assert np.ccy_or(Currency("EUR")) == Currency("EUR")
    assert np.ccy_or_none() is None
    assert np.qty_or(Decimal("10.5")) == Decimal("10.5")
    assert np.qty_or_zero() == Decimal("0")
    assert np.qty_or_none() is None
    assert np.dov_or(Date(2023, 1, 1)) == Date(2023, 1, 1)
    assert np.dov_or_none() is None
