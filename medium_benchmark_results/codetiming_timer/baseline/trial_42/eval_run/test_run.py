import pytest
from codetiming._timer import Timer, TimerError

def test_timer_start_twice_raises():
    # Create a Timer with a no-op logger to avoid console output
    t = Timer(logger=lambda msg: None)

    # First start should set the internal start time
    t.start()
    assert t._start_time is not None, "Timer should record a start time after start()"

    # Second start while running should raise TimerError
    with pytest.raises(TimerError, match="Timer is running"):
        t.start()
