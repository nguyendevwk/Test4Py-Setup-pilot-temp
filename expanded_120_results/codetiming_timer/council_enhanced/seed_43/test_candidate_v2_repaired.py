import pytest
import time
from codetiming._timer import Timer, TimerError

def test_timer_start_stop_and_logging(monkeypatch):
    logs = []

    def logger(msg): logs.append(msg)

    # Mock perf_counter to produce deterministic elapsed time
    times = iter([100.0, 100.5])
    monkeypatch.setattr(time, "perf_counter", lambda: next(times))

    t = Timer(
        name="perf",
        text=lambda secs: f"Elapsed: {secs:.2f}s",
        initial_text=True,
        logger=logger,
    )

    t.start()
    assert logs == ["Timer perf started"]

    elapsed = t.stop()
    assert elapsed == 0.5
    assert logs[-1] == "Elapsed: 0.50s"
    assert Timer.timers.data["perf"] == 0.5

    # Second timing
    times = iter([200.0, 200.3])
    monkeypatch.setattr(time, "perf_counter", lambda: next(times))

    t.start()
    with pytest.raises(TimerError):
        t.start()
    t.stop()
    assert Timer.timers.data["perf"] == pytest.approx(0.8)

    # Stop without start should raise
    t2 = Timer(name="new", logger=logger)
    with pytest.raises(TimerError):
        t2.stop()
