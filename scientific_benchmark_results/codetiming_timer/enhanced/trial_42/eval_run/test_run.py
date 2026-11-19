import pytest
from codetiming._timer import Timer, TimerError

def test_timer_start_twice_raises_error():
    """Calling Timer.start twice without stopping should raise TimerError."""
    t = Timer()
    t.start()
    with pytest.raises(TimerError):
        t.start()
    t.stop()
