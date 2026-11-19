import pytest
from codetiming._timer import Timer, TimerError

def test_timer_start_stop_logs_and_updates(monkeypatch):
    logs = []

    def logger(msg: str) -> None:
        logs.append(msg)

    # Mock time.perf_counter to return deterministic values
    counter = {"value": 0}
    def fake_perf_counter():
        val = counter["value"]
        counter["value"] += 2  # increment by 2 seconds each call
        return val
    monkeypatch.setattr("codetiming._timer.time.perf_counter", fake_perf_counter)

    t = Timer(name="test", initial_text="Timer {name} started", logger=logger)

    # Start the timer: should log the initial text
    t.start()
    assert logs == ["Timer test started"]

    # Stop the timer: should log the elapsed time and set last
    elapsed = t.stop()
    assert elapsed == 2.0
    assert t.last == 2.0
    assert logs[1] == "Elapsed time: 2.0000 seconds"
