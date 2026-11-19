import time
import pytest
from codetiming._timer import Timer


def test_timer_start_stop_logging_and_timers(monkeypatch):
    # Ensure a clean timers registry
    Timer.timers.clear()

    # Capture logger output
    logs = []

    def logger(msg: str) -> None:
        logs.append(msg)

    # Simulate perf_counter returning 100 then 105
    times = iter([100.0, 105.0])
    monkeypatch.setattr(time, "perf_counter", lambda: next(times))

    # Create a timer that logs an initial message and uses a custom format
    t = Timer(name="perf", text="Elapsed: {:0.4f}s", initial_text=True, logger=logger)

    # Start the timer – should log the initial message
    t.start()
    assert logs[0] == "Timer perf started"

    # Stop the timer – should log the elapsed time and update the registry
    elapsed = t.stop()
    assert elapsed == 5.0
    assert logs[1] == "Elapsed: 5.0000s"

    # Verify timer state and registry contents
    assert t.last == 5.0
    assert t._start_time is None
    assert Timer.timers.data["perf"] == 5.0
    assert Timer.timers._timings["perf"] == [5.0]
