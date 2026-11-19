import time
import pytest
from codetiming._timer import Timer, TimerError

def test_timer_start_stop_behavior(monkeypatch):
    # Ensure a clean state for the shared Timers instance
    Timer.timers.clear()

    # Mock perf_counter to produce a deterministic elapsed time of 0.5 seconds
    counter = iter([100.0, 100.5])
    monkeypatch.setattr(time, "perf_counter", lambda: next(counter))

    # Capture logger output via a callable that appends to a list
    logged = []

    # Create a Timer with a custom initial text and logger
    t = Timer(
        name="test",
        text="Elapsed: {:0.4f}s",
        initial_text="Timer {name} started",
        logger=lambda msg: logged.append(msg),
    )

    # Start the timer and verify initial log
    t.start()
    assert logged[0] == "Timer test started"

    # Stop the timer and verify elapsed time log and return value
    elapsed = t.stop()
    assert logged[1] == "Elapsed: 0.5000s"
    assert elapsed == 0.5

    # Verify that the elapsed time was recorded in the shared Timers instance
    assert Timer.timers.total("test") == 0.5

    # Starting an already running timer should raise TimerError
    with pytest.raises(TimerError):
        t.start()

    # Stopping an already stopped timer should raise TimerError
    with pytest.raises(TimerError):
        t.stop()
