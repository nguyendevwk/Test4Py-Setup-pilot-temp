import pytest
from codetiming import Timer

def test_timer_stop_logs_and_updates(monkeypatch):
    # Capture logger output
    logs = []
    def fake_logger(msg: str) -> None:
        logs.append(msg)

    # Mock time.perf_counter to control elapsed time
    times = iter([0.0, 0.5])  # start at 0.0, stop at 0.5
    monkeypatch.setattr("codetiming._timer.time.perf_counter", lambda: next(times))

    # Ensure timers dict is clean
    Timer.timers.clear()

    t = Timer(name="perf", text="Elapsed: {:0.4f}s", logger=fake_logger)
    t.start()
    elapsed = t.stop()

    # Verify elapsed time returned
    assert elapsed == 0.5

    # Verify last field updated
    assert t.last == 0.5

    # Verify logger called once with formatted string
    assert logs == ["Elapsed: 0.5000s"]

    # Verify timers dict updated
    assert Timer.timers.data["perf"] == 0.5
    assert Timer.timers._timings["perf"] == [0.5]
