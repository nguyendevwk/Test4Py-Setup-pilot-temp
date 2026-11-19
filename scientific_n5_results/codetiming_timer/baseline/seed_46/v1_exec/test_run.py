import time
import pytest
from codetiming._timer import Timer, TimerError

def test_timer_start_stop_logs_and_updates_timers(monkeypatch):
    # Capture logger output
    logs = []
    def logger(msg: str) -> None:
        logs.append(msg)

    # Replace Timers.add to record calls
    add_calls = []
    monkeypatch.setattr(Timer.timers, "add", lambda name, elapsed: add_calls.append((name, elapsed)))

    # Create timer with custom logger, initial text, and callable text
    t = Timer(name="test", initial_text="Starting {name}", text=lambda elapsed: f"Elapsed: {elapsed:.2f}s", logger=logger)

    # Start and stop the timer
    t.start()
    elapsed = t.stop()

    # Verify initial log
    assert logs[0] == "Starting test"

    # Verify elapsed log
    assert logs[1].startswith("Elapsed: ")
    assert logs[1].endswith("s")
    # Extract numeric part and compare to elapsed
    numeric = float(logs[1].split(":")[1].strip()[:-1])
    assert pytest.approx(numeric, rel=0.1) == elapsed

    # Verify Timers.add was called with correct arguments
    assert add_calls == [("test", elapsed)]
    assert elapsed > 0.0

    # Ensure calling start again raises TimerError
    with pytest.raises(TimerError, match="Timer is running"):
        t.start()

    # Ensure calling stop again raises TimerError
    with pytest.raises(TimerError, match="Timer is not running"):
        t.stop()
