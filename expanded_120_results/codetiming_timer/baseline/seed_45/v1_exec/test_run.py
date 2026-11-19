import math
import pytest
from codetiming._timer import Timer, TimerError

def test_timer_start_stop_and_logging():
    logs = []
    text = lambda elapsed: f"Elapsed: {elapsed:.2f}s"
    timer = Timer(name='test', text=text, initial_text=True, logger=logs.append)

    timer.start()
    assert logs[0] == "Timer test started"

    timer.stop()
    assert len(logs) == 2
    assert logs[1].startswith("Elapsed:")
    assert timer.last is not None
    assert not math.isnan(timer.last)
    assert timer._start_time is None

    # Starting an already running timer raises TimerError
    timer2 = Timer(name='dup', text=text, initial_text=False, logger=logs.append)
    timer2.start()
    with pytest.raises(TimerError):
        timer2.start()
    timer2.stop()

    # Stopping without starting raises TimerError
    timer3 = Timer(name='no_start', text=text, initial_text=False, logger=logs.append)
    with pytest.raises(TimerError):
        timer3.stop()
