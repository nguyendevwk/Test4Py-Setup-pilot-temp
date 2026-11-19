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
    timers.add("beta", 2.5)
    timers.add("beta", 3.5)

    # Verify internal data aggregation
    assert timers.data["alpha"] == 4.0
    assert timers.data["beta"] == 8.5

    # Count
    assert timers.count("alpha") == 2
    assert timers.count("beta") == 3

    # Total
    assert timers.total("alpha") == 4.0
    assert timers.total("beta") == 8.5

    # Min, Max
    assert timers.min("alpha") == 1.0
    assert timers.max("alpha") == 3.0
    assert timers.min("beta") == 2.5
    assert timers.max("beta") == 3.5

    # Mean
    assert timers.mean("alpha") == statistics.mean([1.0, 3.0])
    assert timers.mean("beta") == statistics.mean([2.5, 2.5, 3.5])

    # Median
    assert timers.median("alpha") == statistics.median([1.0, 3.0])
    assert timers.median("beta") == statistics.median([2.5, 2.5, 3.5])

    # Standard deviation
    assert math.isclose(timers.stdev("alpha"), statistics.stdev([1.0, 3.0]), rel_tol=1e-9)
    assert math.isclose(timers.stdev("beta"), statistics.stdev([2.5, 2.5, 3.5]), rel_tol=1e-9)

def test_clear_resets_state():
    timers = Timers()
    timers.add("gamma", 5.0)
    timers.add("gamma", 7.0)
    timers.add("delta", 1.0)

    # Ensure data present before clear
    assert "gamma" in timers.data
    assert "delta" in timers.data
    assert timers.data["gamma"] == 12.0
    assert timers.data["delta"] == 1.0

    # Clear timers
    timers.clear()

    # After clear, data and timings should be empty
    assert timers.data == {}
    assert timers._timings == {}
    with pytest.raises(KeyError):
        timers.total("gamma")

def test_errors_and_disallowed_assignment():
    timers = Timers()
    timers.add("epsilon", 2.0)

    # Accessing a non-existent timer should raise KeyError
    with pytest.raises(KeyError):
        timers.total("nonexistent")

    # Attempting to set an item directly should raise TypeError
    with pytest.raises(TypeError) as excinfo:
        timers["epsilon"] = 3.0
    assert "does not support item assignment" in str(excinfo.value)

    # Standard deviation with only one value should return NaN
    assert math.isnan(timers.stdev("epsilon"))
