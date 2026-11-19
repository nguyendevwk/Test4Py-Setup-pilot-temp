import math
import statistics
import pytest
from codetiming._timers import Timers


def test_add_and_statistics():
    timers = Timers()
    # Add multiple timings for the same timer
    timers.add("load", 1.0)
    timers.add("load", 2.0)
    timers.add("load", 3.0)

    # Verify internal data aggregation
    assert timers.data["load"] == 6.0
    assert timers._timings["load"] == [1.0, 2.0, 3.0]

    # Check statistical methods
    assert timers.count("load") == 3
    assert timers.total("load") == 6.0
    assert timers.min("load") == 1.0
    assert timers.max("load") == 3.0
    assert timers.mean("load") == statistics.mean([1.0, 2.0, 3.0])
    assert timers.median("load") == statistics.median([1.0, 2.0, 3.0])
    assert math.isclose(timers.stdev("load"), statistics.stdev([1.0, 2.0, 3.0]), rel_tol=1e-9)


def test_empty_timer_raises_key_error():
    timers = Timers()
    # No timings added yet; accessing statistics should raise KeyError
    with pytest.raises(KeyError):
        timers.count("empty")
    with pytest.raises(KeyError):
        timers.total("empty")
    with pytest.raises(KeyError):
        timers.min("empty")
    with pytest.raises(KeyError):
        timers.max("empty")
    with pytest.raises(KeyError):
        timers.mean("empty")
    with pytest.raises(KeyError):
        timers.median("empty")
    with pytest.raises(KeyError):
        timers.stdev("empty")


def test_setitem_disallowed():
    timers = Timers()
    # Direct item assignment should raise TypeError
    with pytest.raises(TypeError) as excinfo:
        timers["direct"] = 5.0
    assert "does not support item assignment" in str(excinfo.value)
