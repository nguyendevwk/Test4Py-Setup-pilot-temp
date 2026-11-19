import pytest
from genty.genty_repeat import genty_repeat

def test_genty_repeat_negative_count_raises():
    """genty_repeat should raise ValueError for negative count."""
    with pytest.raises(ValueError) as excinfo:
        genty_repeat(-1)
    assert str(excinfo.value) == (
        "Really? Can't have -1 iterations. Please pick a value >= 0."
    )
