import pytest
from codetiming._timer import Timer

def test_timer_stop_logging_and_timers(monkeypatch):
    logs = []

    # Ensure a clean timers dictionary
    Timer.timers.clear()

    t = Timer(
        name="test",
        text="Elapsed: {:0.4f}s",
        logger=lambda s: logs.append(s),
    )

    # Mock perf_counter to control elapsed time
    counter = iter([100.0, 110.0])  # start at 100, stop at 110
    monkeypatch.setattr("codetiming._timer.time.perf_counter", lambda: next(counter))

    t.start()
    elapsed = t.stop()

    assert elapsed == 10.0
    assert logs == ["Elapsed: 10.0000s"]
    assert t.last == 10.0
    assert Timer.timers.data["test"] == 10.0
