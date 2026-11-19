import time
import pytest
from codetiming._timer import Timer, TimerError

def test_timer_start_stop_logs_and_updates_timers():
    logged = []

    def logger(msg: str) -> None:
        logged.append(msg)

    t = Timer(name="perf", text="Elapsed: {:0.4f}s", initial_text=True, logger=logger)

    # Start the timer and verify initial log
    t.start()
    assert logged[0] == "Timer perf started"

    # Wait a short time to get a measurable elapsed time
    time.sleep(0.01)

    # Stop the timer and verify returned value and log
    elapsed = t.stop()
    assert elapsed > 0
    assert logged[1].startswith("Elapsed: ")
    assert logged[1].endswith("s")

    # Verify that the timer's total time is recorded correctly
    assert Timer.timers.total("perf") == elapsed
