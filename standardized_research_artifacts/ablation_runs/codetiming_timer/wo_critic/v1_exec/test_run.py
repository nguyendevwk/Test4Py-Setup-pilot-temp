import time

import pytest

from codetiming._timer import Timer, TimerError


def test_timer_start_stop_and_errors():
    # Capture logger output
    logs = []

    def logger(msg: str) -> None:
        logs.append(msg)

    # Ensure a clean timers registry
    Timer.timers.clear()

    # Create a timer with a custom initial message
    t = Timer(name="perf", initial_text="Timer {name} started", logger=logger)

    # Start the timer and verify the initial log
    t.start()
    assert logs[-1] == "Timer perf started"

    # Wait a short time to create measurable elapsed time
    time.sleep(0.01)

    # Stop the timer and verify the elapsed time and log
    elapsed = t.stop()
    assert isinstance(elapsed, float)
    assert elapsed > 0
    assert logs[-1].startswith("Elapsed time:")
    assert Timer.timers.total("perf") == pytest.approx(elapsed)

    # Verify that starting an already running timer raises TimerError
    t.start()
    with pytest.raises(TimerError):
        t.start()
    t.stop()

    # Verify that stopping without starting raises TimerError
    t2 = Timer(name="no_start", logger=logger)
    with pytest.raises(TimerError):
        t2.stop()
