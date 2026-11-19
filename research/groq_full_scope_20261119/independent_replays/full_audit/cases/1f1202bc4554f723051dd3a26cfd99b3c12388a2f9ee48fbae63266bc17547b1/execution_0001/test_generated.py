import pytest
from flutes.iterator import drop

def test_drop_normal():
    """Drop a middle segment from a list."""
    data = list(range(10))
    it = drop(3, data)
    assert list(it) == [3, 4, 5, 6, 7, 8, 9]

def test_drop_boundary_empty():
    """Dropping more elements than present yields an empty iterator."""
    data = [1, 2]
    it = drop(5, data)
    assert list(it) == []

def test_drop_negative_raises():
    """Negative drop count should raise ValueError."""
    with pytest.raises(ValueError) as exc:
        list(drop(-1, [1, 2, 3]))
    assert "`n` should be non-negative" in str(exc.value)
