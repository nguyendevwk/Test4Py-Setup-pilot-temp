import pytest
from genty.genty_repeat import genty_repeat

def test_genty_repeat_negative_count_raises_value_error():
    with pytest.raises(ValueError) as excinfo:
        genty_repeat(-5)
    assert "Really? Can't have -5 iterations" in str(excinfo.value)
