import pytest
from codetiming._timer import Timer, TimerError

def test_timer_start_stop_logging_and_timers(monkeypatch):
    # deterministic perf_counter values: start1, stop1, start2, stop2
    perf_counter_values = iter([1.0, 2.5, 3.0, 4.5])
    monkeypatch.setattr("codetiming._timer.time.perf_counter", lambda: next(perf_counter_values))

    Timer.timers.clear()
    logged = []

    t = Timer(
        name="test",
        text="Elapsed: {:0.4f}s",
        initial_text="Starting timer {name}",
        logger=logged.append,
    )

    # first run
    t.start()
    assert logged == ["Starting timer test"]
    assert t._start_time is not None
    elapsed1 = t.stop()
    assert elapsed1 == 1.5
    assert t.last == 1.5
    assert logged == ["Starting timer test", "Elapsed: 1.5000s"]
    assert Timer.timers.total("test") == 1.5
    assert Timer.timers.count("test") == 1

    # second run
    t.start()
    with pytest.raises(TimerError, match="Timer is running"):
        t.start()
    elapsed2 = t.stop()
    assert elapsed2 == 1.5
    assert t.last == 1.5
    assert logged == ["Starting timer test", "Elapsed: 1.5000s",
                      "Starting timer test", "Elapsed: 1.5000s"]
    assert Timer.timers.total("test") == 3.0
    assert Timer.timers.count("test") == 2
    with pytest.raises(TimerError, match="Timer is not running"):
        t.stop()
