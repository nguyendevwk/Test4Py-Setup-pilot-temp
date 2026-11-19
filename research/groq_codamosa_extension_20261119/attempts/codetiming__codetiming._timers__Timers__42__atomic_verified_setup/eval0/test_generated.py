import math
import statistics
import pytest
from codetiming._timers import Timers


def test_add_and_statistics():
    timers = Timers()
    # Add three timings for the same timer
    timers.add("load", 1.0)
    timers.add("load", 2.0)
    timers.add("load", 3.0)

    # Verify internal data aggregation
    assert timers.data["load"] == 6.0
    assert timers._timings["load"] == [1.0, 2.0, 3.0]

    # Count, total, min, max, mean, median
    assert timers.count("load") == 3
    assert timers.total("load") == 6.0
    assert timers.min("load") == 1.0
    assert timers.max("load") == 3.0
    assert timers.mean("load") == statistics.mean([1.0, 2.0, 3.0])
    assert timers.median("load") == statistics.median([1.0, 2.0, 3.0])

    # Stdev with at least two values
    assert timers.stdev("load") == statistics.stdev([1.0, 2.0, 3.0])


def test_setitem_raises_type_error():
    timers = Timers()
    timers.add("compute", 0.5)
    with pytest.raises(TypeError) as excinfo:
        timers["compute"] = 1.0
    assert "does not support item assignment" in str(excinfo.value)


def test_stdev_boundary_and_missing_timer():
    timers = Timers()
    # Single value: stdev should be NaN
    timers.add("single", 42.0)
    assert math.isnan(timers.stdev("single"))

    # No values: KeyError
    with pytest.raises(KeyError):
        timers.stdev("missing")
