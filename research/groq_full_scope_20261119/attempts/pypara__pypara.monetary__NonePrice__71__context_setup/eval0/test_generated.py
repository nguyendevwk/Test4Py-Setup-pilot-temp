import pytest
from decimal import Decimal
from pypara.monetary import NonePrice, NoPrice, NoMoney
from pypara.currencies import Currency
from pypara.commons.zeitgeist import Date

# Helper currency and date for tests
USD = Currency("USD")
TODAY = Date.today()


def test_noneprice_properties_and_equality():
    """NonePrice should report undefined status and compare equal only to itself."""
    np = NonePrice()
    # defined/undefined flags
    assert not np.defined
    assert np.undefined
    # boolean conversion
    assert bool(np) is False
    # equality only with same class
    assert np == NonePrice()
    assert np != NoPrice()
    # numeric conversions raise TypeError
    with pytest.raises(TypeError):
        float(np)
    with pytest.raises(TypeError):
        int(np)


def test_noneprice_arithmetic_and_comparisons():
    """Arithmetic operations with NonePrice should propagate or return the other operand."""
    np = NonePrice()
    # addition returns the other operand
    assert np + 5 == 5
    assert 5 + np == 5
    # subtraction returns negative of the other operand
    assert np - 5 == -5
    assert 5 - np == -5
    # multiplication/division return NonePrice
    assert np * 3 == np
    assert np / 3 == np
    # comparisons: NonePrice is less than any defined price, greater than none
    defined_price = NoPrice()  # placeholder for a defined price
    assert np < defined_price
    assert np <= defined_price
    assert np > NoPrice() is False
    assert np >= NoPrice() is True


def test_noneprice_conversion_and_or_else():
    """Conversion should be identity; or_else should evaluate the supplied callable."""
    np = NonePrice()
    # convert returns itself
    assert np.convert(USD) is np
    # or_else evaluates the function and returns its result
    called = False

    def factory():
        nonlocal called
        called = True
        return NoPrice()

    result = np.or_else(factory)
    assert called is True
    assert isinstance(result, NoPrice)
