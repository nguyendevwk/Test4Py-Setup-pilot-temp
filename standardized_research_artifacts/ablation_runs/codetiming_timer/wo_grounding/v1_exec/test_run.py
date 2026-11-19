import time
import pytest
from codetiming._timer import Timer, TimerError

def test_timer_start_stop_logging_and_timers():
    logs = []

    # Create a timer with custom logger and messages
    timer = Timer(
        name="test_timer",
        initial_text="Timer {name} started",
        text=lambda t: f"Elapsed: {t:.2f}s",
        logger=logs.append,
    )

    # Start the timer and verify initial log
    timer.start()
    assert logs[0] == "Timer test_timer started"

    # Stop the timer after a short delay and verify elapsed log
    time.sleep(0.01)
    elapsed = timer.stop()
    assert logs[1].startswith("Elapsed: ")
    assert elapsed > 0

    # Verify that the elapsed time was recorded in the class-wide Timers
    recorded = Timer.timers.get("test_timer")
    assert recorded == [elapsed]

    # Verify that starting an already running timer raises TimerError
    timer.start()
    with pytest.raises(TimerError):
        timer.start()
    timer.stop()

    # Verify that stopping an already stopped timer raises TimerError
    with pytest.raises(TimerError):
        timer.stop()
