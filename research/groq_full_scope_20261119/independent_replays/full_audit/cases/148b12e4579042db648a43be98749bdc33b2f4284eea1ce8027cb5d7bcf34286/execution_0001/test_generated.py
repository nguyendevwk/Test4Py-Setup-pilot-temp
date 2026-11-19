import math
import statistics
import pytest
from codetiming._timers import Timers


def test_add_and_basic_stats():
    timers = Timers()
    # Add multiple timings for two different timers
    timers.add("alpha", 1.0)
    timers.add("alpha", 3.0)
    timers.add("beta", 2.5)

    # Verify internal data aggregation
    assert timers.data["alpha"] == 4.0
    assert timers.data["beta"] == 2.5

    # Count, total, min, max, mean, median
    assert timers.count("alpha") == 2
    assert timers.total("alpha") == 4.0
    assert timers.min("alpha") == 1.0
    assert timers.max("alpha") == 3.0
    assert timers.mean("alpha") == statistics.mean([1.0, 3.0])
    assert timers.median("alpha") == statistics.median([1.0, 3.0])

    # Single value timer
    assert timers.count("beta") == 1
    assert timers.total("beta") == 2.5
    assert timers.min("beta") == 2.5
    assert timers.max("beta") == 2.5
    assert timers.mean("beta") == 2.5
    assert timers.median("beta") == 2.5


def test_stdev_and_clear():
    timers = Timers()
    timers.add("gamma", 1.0)
    timers.add("gamma", 4.0)
    timers.add("gamma", 7.0)

    # Standard deviation with at least two values
    expected_stdev = statistics.stdev([1.0, 4.0, 7.0])
    assert timers.stdev("gamma") == expected_stdev

    # Clear all timers
    timers.clear()
    assert timers.data == {}
    assert timers._timings == {}

    # After clearing, accessing stats should raise KeyError
    with pytest.raises(KeyError):
        timers.total("gamma")


def test_errors_and_assignment_restriction():
    timers = Timers()
    timers.add("delta", 5.0)

    # Accessing non-existent timer should raise KeyError
    with pytest.raises(KeyError):
        timers.count("nonexistent")

    # Attempting to set item directly should raise TypeError
    with pytest.raises(TypeError) as excinfo:
        timers["delta"] = 10.0
    assert "does not support item assignment" in str(excinfo.value)
