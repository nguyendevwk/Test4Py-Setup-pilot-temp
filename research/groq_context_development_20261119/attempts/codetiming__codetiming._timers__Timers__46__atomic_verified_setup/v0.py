import math
import statistics
import pytest
from codetiming._timers import Timers


def test_add_and_statistics(tmp_path):
    timers = Timers()
    timers.add("load", 1.0)
    timers.add("load", 2.0)
    timers.add("load", 3.0)

    # Basic aggregate values
    assert timers.count("load") == 3
    assert timers.total("load") == 6.0
    assert timers.min("load") == 1.0
    assert timers.max("load") == 3.0
    assert timers.mean("load") == statistics.mean([1.0, 2.0, 3.0])
    assert timers.median("load") == statistics.median([1.0, 2.0, 3.0])

    # Standard deviation
    assert timers.stdev("load") == statistics.stdev([1.0, 2.0, 3.0])

    # Ensure data dictionary reflects summed value
    assert timers.data["load"] == 6.0

    # Clearing timers resets state
    timers.clear()
    assert timers.data == {}
    with pytest.raises(KeyError):
        timers.count("load")


def test_key_error_on_missing_timer():
    timers = Timers()
    with pytest.raises(KeyError):
        timers.total("missing")
    with pytest.raises(KeyError):
        timers.min("missing")
    with pytest.raises(KeyError):
        timers.stdev("missing")


def test_stdev_single_value_returns_nan():
    timers = Timers()
    timers.add("single", 42.0)
    result = timers.stdev("single")
    assert math.isnan(result)
