import pytest
from codetiming._timer import Timer, TimerError

def test_start_twice_raises():
    """Starting a Timer that is already running should raise TimerError."""
    # Use a no‑op logger to avoid side effects
    t = Timer(name="demo", logger=lambda msg: None)
    t.start()
    # The timer is now running; attempting to start again must raise
    with pytest.raises(TimerError, match="Timer is running"):
        t.start()
