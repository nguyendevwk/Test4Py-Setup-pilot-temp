import pytest
from decimal import Decimal
from pypara.monetary import NonePrice, NoMoney
from pypara.currencies import Currency
from pypara.commons.zeitgeist import Date

def test_noneprice_basic_properties_and_comparisons():
    np = NonePrice()
    # Basic flags
    assert np.defined is False
    assert np.undefined is True
    assert bool(np) is False
    # Equality only with same class
    assert np == NonePrice()
    assert np != 42
    # Comparisons with defined price (using NoMoney as placeholder)
    assert np < NoMoney
    assert np <= NoMoney
    assert np > NoMoney is False
    assert np >= NoMoney
    # Arithmetic with defined price
    assert np + NoMoney == NoMoney
    assert np - NoMoney == -NoMoney
    assert np * 2 == np
    assert np / 3 == np
    assert np // 4 == np
    # Absolute value and sign
    assert abs(np) is np
    assert -np is np
    assert +np is np

def test_noneprice_or_else_and_mapping():
    np = NonePrice()
    # or_else should call the supplier
    called = False
    def supplier():
        nonlocal called
        called = True
        return NonePrice()
    result = np.or_else(supplier)
    assert called is True
    assert result is np
    # fmap returns self
    assert np.fmap(lambda x: x) is np
    # dimap returns the supplied default
    assert np.dimap(lambda x: x, lambda: 123) == 123

def test_noneprice_conversion_and_exceptions():
    np = NonePrice()
    # Converting returns self
    assert np.convert(Currency('USD')) is np
    # Accessing money raises no error but returns NoMoney
    assert np.money is NoMoney
    # Quantity and date defaults
    assert np.qty_or(Decimal('10.5')) == Decimal('10.5')
    assert np.qty_or_zero() == Decimal('0')
    assert np.dov_or(Date(2023, 1, 1)) == Date(2023, 1, 1)
    # as_float and as_integer raise TypeError
    with pytest.raises(TypeError):
        np.as_float()
    with pytest.raises(TypeError):
        np.as_integer()
