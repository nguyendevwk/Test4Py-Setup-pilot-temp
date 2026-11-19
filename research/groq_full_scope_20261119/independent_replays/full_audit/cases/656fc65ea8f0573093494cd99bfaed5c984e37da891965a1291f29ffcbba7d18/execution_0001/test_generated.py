import pytest
from flutes.iterator import drop

def test_drop_normal():
    """Dropping a few elements from a list yields the expected remainder."""
    data = [10, 20, 30, 40, 50]
    result = list(drop(2, data))
    assert result == [30, 40, 50], "Expected to drop the first two elements"

def test_drop_exhaustive():
    """Dropping more elements than the iterable length yields an empty iterator."""
    data = [1, 2]
    result = list(drop(5, data))
    assert result == [], "Expected an empty list when dropping beyond length"

def test_drop_negative_n():
    """Providing a negative number of elements to drop raises ValueError."""
    with pytest.raises(ValueError) as excinfo:
        list(drop(-1, [1, 2, 3]))
    assert "`n` should be non-negative" in str(excinfo.value)
