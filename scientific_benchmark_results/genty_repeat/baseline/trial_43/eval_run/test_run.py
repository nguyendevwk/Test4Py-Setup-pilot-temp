import pytest
from genty.genty_repeat import genty_repeat

def test_genty_repeat_negative_raises():
    """genty_repeat should raise ValueError when count is negative."""
    with pytest.raises(ValueError) as excinfo:
        genty_repeat(-1)
    assert "Can't have -1 iterations" in str(excinfo.value)
