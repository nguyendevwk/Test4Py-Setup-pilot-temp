import pytest
from codetiming._timer import Timer, TimerError

def test_timer_start_twice_raises():
    """Starting a Timer that is already running should raise TimerError."""
    timer = Timer()
    timer.start()
    with pytest.raises(TimerError, match="Timer is running"):
        timer.start()
