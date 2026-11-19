import math
import statistics
import pytest
from codetiming._timers import Timers


def test_add_and_basic_stats():
    timers = Timers()
    # Add multiple timings for the same timer
    timers.add("load", 1.0)
    timers.add("load", 2.0)
    timers.add("load", 3.0)

    # Verify internal data aggregation
    assert timers.data["load"] == 6.0
    assert timers._timings["load"] == [1.0, 2.0, 3.0]

    # Basic statistics
    assert timers.count("load") == 3
    assert timers.total("load") == 6.0
    assert timers.min("load") == 1.0
    assert timers.max("load") == 3.0
    assert timers.mean("load") == statistics.mean([1.0, 2.0, 3.0])
    assert timers.median("load") == statistics.median([1.0, 2.0, 3.0])
    assert math.isclose(timers.stdev("load"), statistics.stdev([1.0, 2.0, 3.0]), rel_tol=1e-9)


def test_stdev_single_and_no_timings():
    timers = Timers()
    timers.add("single", 5.0)

    # Standard deviation with a single value should be NaN
    assert math.isnan(timers.stdev("single"))

    # Requesting stats for a non-existent timer raises KeyError
    with pytest.raises(KeyError):
        timers.mean("missing")
    with pytest.raises(KeyError):
        timers.stdev("missing")


def test_item_assignment_and_clear():
    timers = Timers()
    timers.add("foo", 1.5)

    # Direct item assignment is disallowed
    with pytest.raises(TypeError):
        timers["foo"] = 2.0

    # Clear should reset both data and timings
    timers.clear()
    assert timers.data == {}
    assert timers._timings == {}
    # After clearing, accessing stats should raise KeyError
    with pytest.raises(KeyError):
        timers.total("foo")
