import math
import statistics
import pytest
from codetiming._timers import Timers


def test_add_and_statistics():
    timers = Timers()
    # Add several timings for the same timer
    timers.add("load", 1.0)
    timers.add("load", 2.0)
    timers.add("load", 3.0)

    # Verify internal data aggregation
    assert timers.data["load"] == 6.0
    assert timers._timings["load"] == [1.0, 2.0, 3.0]

    # Count, total, min, max, mean, median, stdev
    assert timers.count("load") == 3
    assert timers.total("load") == 6.0
    assert timers.min("load") == 1.0
    assert timers.max("load") == 3.0
    assert timers.mean("load") == statistics.mean([1.0, 2.0, 3.0])
    assert timers.median("load") == statistics.median([1.0, 2.0, 3.0])
    assert math.isclose(timers.stdev("load"), statistics.stdev([1.0, 2.0, 3.0]), rel_tol=1e-9)


def test_error_on_setitem_and_missing_timer():
    timers = Timers()
    # Setting an item directly should raise TypeError
    with pytest.raises(TypeError, match="does not support item assignment"):
        timers["load"] = 5.0

    # Accessing statistics on a non‑existent timer should raise KeyError
    with pytest.raises(KeyError, match="load"):
        timers.total("load")
    with pytest.raises(KeyError, match="load"):
        timers.stdev("load")


def test_stdev_boundary_single_value():
    timers = Timers()
    timers.add("single", 42.0)
    # With only one timing, stdev should return NaN
    result = timers.stdev("single")
    assert math.isnan(result)
    # Other statistics should still work
    assert timers.count("single") == 1
    assert timers.total("single") == 42.0
    assert timers.mean("single") == 42.0
