import time
import pytest
from codetiming import Timer

def test_stop_logs_callable_text_and_updates_timers():
    # Ensure a clean timers state
    Timer.timers.clear()

    logged = []

    def logger(msg: str) -> None:
        logged.append(msg)

    # Use a callable text that formats the elapsed time
    t = Timer(name="test", text=lambda elapsed: f"Elapsed: {elapsed:.2f}s", logger=logger)

    # No initial log because initial_text is False
    assert logged == []

    # Start and stop the timer
    t.start()
    time.sleep(0.01)  # sleep 10 ms
    elapsed = t.stop()

    # Logger should have been called once with the formatted string
    assert len(logged) == 1
    assert logged[0] == f"Elapsed: {elapsed:.2f}s"

    # The returned elapsed time should be close to the sleep duration
    assert elapsed > 0
    assert elapsed < 0.02  # allow some overhead

    # The timer's internal record should be updated
    assert Timer.timers.total("test") == pytest.approx(elapsed, rel=0.1)
    assert Timer.timers.count("test") == 1
