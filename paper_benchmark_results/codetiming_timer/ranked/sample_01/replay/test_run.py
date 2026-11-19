import pytest
from codetiming._timer import Timer, TimerError

def test_timer_start_twice_raises():
    t = Timer(name="test", logger=lambda msg: None)
    t.start()
    with pytest.raises(TimerError):
        t.start()
