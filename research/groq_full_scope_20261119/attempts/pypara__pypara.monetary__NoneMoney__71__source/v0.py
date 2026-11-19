import pytest
from decimal import Decimal
from pypara.monetary import NoneMoney
from pypara.currencies import Currency
from pypara.commons.zeitgeist import Date

def test_comparison_and_boolean_behavior():
    nm = NoneMoney()
    # Boolean conversion
    assert not nm
    # Equality only with other NoneMoney
    assert nm == NoneMoney()
    assert nm != 5
    # Ordering comparisons
    assert nm < NoneMoney()  # other defined? both undefined, so True
    assert nm <= NoneMoney()  # always True
    assert not nm > NoneMoney()
    assert nm >= NoneMoney()  # other undefined? True

def test_arithmetic_identity_and_identity_operations():
    nm = NoneMoney()
    # Adding any Money returns the other
    other = NoneMoney()
    assert nm + other is other
    # Subtracting returns negative of other
    assert nm - other == -other
    # Scalar operations return self
    assert nm * 2 is nm
    assert nm / 3 is nm
    assert nm // 4 is nm
    # Negative and positive return self
    assert -nm is nm
    assert +nm is nm
    # or_else executes the supplied function
    assert nm.or_else(lambda: NoneMoney()) is NoneMoney()

def test_error_and_default_behavior():
    nm = NoneMoney()
    # Converting to a currency returns self
    usd = Currency("USD")
    assert nm.convert(usd) is nm
    # Quantity and date defaults
    assert nm.qty_or(Decimal("10.5")) == Decimal("10.5")
    assert nm.qty_or_zero() == Decimal("0")
    assert nm.dov_or(Date(2020, 1, 1)) == Date(2020, 1, 1)
    # Accessing price raises no error (returns NoPrice)
    assert nm.price is not None
    # Attempting to get float or int raises TypeError
    with pytest.raises(TypeError):
        float(nm)
    with pytest.raises(TypeError):
        int(nm)
