import pytest
from types import SimpleNamespace
from decimal import Decimal

# Import the target class from the package
from pypara.monetary import NonePrice, NoMoney


def test_noneprice_defined_and_undefined_flags():
    """NonePrice should report correct defined/undefined status."""
    np = NonePrice()
    assert np.defined is False
    assert np.undefined is True
    # Boolean conversion should be False
    assert bool(np) is False
    # Equality with another NonePrice instance
    assert np == NonePrice()
    # Equality with a different type should be False
    assert np != 42


def test_noneprice_arithmetic_and_conversion():
    """Arithmetic operations on NonePrice should return expected results."""
    np = NonePrice()
    # Adding a defined price (mocked with defined=True) returns the other operand
    defined_price = SimpleNamespace(defined=True, __class__=object)
    assert np + defined_price is defined_price
    # Subtracting returns the negation of the other operand
    assert np - defined_price == -defined_price
    # Multiplication, division, floor division should return the same NonePrice instance
    assert np * 5 is np
    assert np / 2 is np
    assert np // 3 is np
    # Converting to money returns NoMoney
    assert np.money is NoMoney
    # Converting to float or int should raise TypeError
    with pytest.raises(TypeError):
        float(np)
    with pytest.raises(TypeError):
        int(np)
    # Converting to a different currency should return the same instance
    dummy_currency = SimpleNamespace(name="USD")
    assert np.with_ccy(dummy_currency) is np
    # Quantity and date defaults
    assert np.qty_or(Decimal("10.5")) == Decimal("10.5")
    assert np.qty_or_zero() == Decimal("0")
    assert np.dov_or("2023-01-01") == "2023-01-01"


def test_noneprice_comparison_and_or_else():
    """Comparison operators and or_else should behave as specified."""
    np = NonePrice()
    # lt returns other.defined
    defined_price = SimpleNamespace(defined=True)
    undefined_price = SimpleNamespace(defined=False)
    assert (np < defined_price) is True
    assert (np < undefined_price) is False
    # lte always True
    assert (np <= defined_price) is True
    assert (np <= undefined_price) is True
    # gt always False
    assert (np > defined_price) is False
    # gte returns other.undefined
    assert (np >= defined_price) is False
    assert (np >= undefined_price) is True
    # or_else should execute the supplied callable
    called = False
    def factory():
        nonlocal called
        called = True
        return NonePrice()
    result = np.or_else(factory)
    assert called is True
    assert result is np
