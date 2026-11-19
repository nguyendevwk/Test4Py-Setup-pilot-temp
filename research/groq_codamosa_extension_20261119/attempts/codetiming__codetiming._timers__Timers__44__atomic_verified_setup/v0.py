import math
import statistics
import pytest
from codetiming._timers import Timers


def test_add_and_statistics(tmp_path):
    timers = Timers()
    timers.add("load", 1.0)
    timers.add("load", 2.0)
    timers.add("load", 3.0)

    # Basic statistics
    assert timers.count("load") == 3
    assert timers.total("load") == 6.0
    assert timers.min("load") == 1.0
    assert timers.max("load") == 3.0
    assert timers.mean("load") == statistics.mean([1.0, 2.0, 3.0])
    assert timers.median("load") == statistics.median([1.0, 2.0, 3.0])
    # Standard deviation
    assert timers.stdev("load") == statistics.stdev([1.0, 2.0, 3.0])

    # Ensure internal data is updated correctly
    assert timers.data["load"] == 6.0
    assert timers._timings["load"] == [1.0, 2.0, 3.0]


def test_missing_timer_raises_key_error():
    timers = Timers()
    with pytest.raises(KeyError, match="missing_timer"):
        timers.count("missing_timer")
    with pytest.raises(KeyError, match="missing_timer"):
        timers.total("missing_timer")
    with pytest.raises(KeyError, match="missing_timer"):
        timers.min("missing_timer")
    with pytest.raises(KeyError, match="missing_timer"):
        timers.max("missing_timer")
    with pytest.raises(KeyError, match="missing_timer"):
        timers.mean("missing_timer")
    with pytest.raises(KeyError, match="missing_timer"):
        timers.median("missing_timer")
    with pytest.raises(KeyError, match="missing_timer"):
        timers.stdev("missing_timer")


def test_stdev_single_value_returns_nan():
    timers = Timers()
    timers.add("single", 42.0)
    # With only one timing, stdev should return NaN
    result = timers.stdev("single")
    assert math.isnan(result)
    # Other statistics should still work
    assert timers.count("single") == 1
    assert timers.total("single") == 42.0
    assert timers.mean("single") == 42.0
