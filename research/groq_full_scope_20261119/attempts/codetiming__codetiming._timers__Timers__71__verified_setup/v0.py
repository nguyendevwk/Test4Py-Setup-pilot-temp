import math
import statistics
import pytest
from codetiming._timers import Timers


def test_add_and_basic_stats():
    timers = Timers()
    # Add multiple timings for two timers
    timers.add("alpha", 1.0)
    timers.add("alpha", 3.0)
    timers.add("beta", 2.5)

    # Basic counts
    assert timers.count("alpha") == 2
    assert timers.count("beta") == 1

    # Totals
    assert timers.total("alpha") == 4.0
    assert timers.total("beta") == 2.5

    # Min/max
    assert timers.min("alpha") == 1.0
    assert timers.max("alpha") == 3.0
    assert timers.min("beta") == 2.5
    assert timers.max("beta") == 2.5

    # Mean and median
    assert timers.mean("alpha") == statistics.mean([1.0, 3.0])
    assert timers.median("alpha") == statistics.median([1.0, 3.0])
    assert timers.mean("beta") == 2.5
    assert timers.median("beta") == 2.5

    # Standard deviation: single value yields NaN
    assert math.isnan(timers.stdev("beta"))
    # Two values: compute stdev
    assert timers.stdev("alpha") == statistics.stdev([1.0, 3.0])


def test_clear_resets_state():
    timers = Timers()
    timers.add("gamma", 4.0)
    timers.add("gamma", 6.0)
    timers.add("delta", 1.0)

    # Ensure data present
    assert timers.count("gamma") == 2
    assert timers.total("delta") == 1.0

    # Clear all timers
    timers.clear()

    # After clear, data structures should be empty
    assert timers.data == {}
    assert timers._timings == {}

    # Operations on cleared timers should raise KeyError
    with pytest.raises(KeyError):
        timers.total("gamma")
    with pytest.raises(KeyError):
        timers.mean("delta")


def test_invalid_assignment_and_missing_timer():
    timers = Timers()
    timers.add("epsilon", 5.0)

    # Direct assignment should raise TypeError
    with pytest.raises(TypeError, match="does not support item assignment"):
        timers["epsilon"] = 10.0

    # Applying function to non-existent timer should raise KeyError
    with pytest.raises(KeyError, match="epsilon"):
        timers.apply(sum, name="epsilon")  # existing, should work
    with pytest.raises(KeyError, match="zeta"):
        timers.apply(sum, name="zeta")  # non-existent
