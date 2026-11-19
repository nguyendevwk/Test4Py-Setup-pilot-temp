import time
import pytest
from codetiming._timer import Timer, TimerError

def test_timer_start_stop_logging_and_timers():
    logs = []

    timer = Timer(
        name="test_timer",
        initial_text="Timer {name} started",
        text=lambda t: f"Elapsed: {t:.2f}s",
        logger=logs.append,
    )

    timer.start()
    assert logs[0] == "Timer test_timer started"

    time.sleep(0.01)
    elapsed = timer.stop()
    assert logs[1].startswith("Elapsed: ")
    assert elapsed > 0

    assert isinstance(Timer.timers, dict)
    recorded = Timer.timers.get("test_timer")
    assert recorded == elapsed

    timer.start()
    with pytest.raises(TimerError):
        timer.start()
    timer.stop()

    with pytest.raises(TimerError):
        timer.stop()
