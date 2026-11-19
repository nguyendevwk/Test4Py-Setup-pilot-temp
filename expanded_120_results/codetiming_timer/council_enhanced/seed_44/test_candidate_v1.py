import pytest
from codetiming._timer import Timer, TimerError

def test_timer_start_stop_logging_and_timers(monkeypatch):
    # Prepare a deterministic perf_counter sequence: 1.0 on start, 2.5 on stop
    perf_counter_values = iter([1.0, 2.5])
    monkeypatch.setattr("codetiming._timer.time.perf_counter", lambda: next(perf_counter_values))

    # Reset shared timers state
    Timer.timers.clear()

    # Logger that records messages
    logged = []

    # Create Timer with custom text and initial_text
    t = Timer(
        name="test",
        text="Elapsed: {:0.4f}s",
        initial_text="Starting timer {name}",
        logger=logged.append,
    )

    # Start the timer and verify initial log
    t.start()
    assert logged == ["Starting timer test"]
    assert t._start_time is not None

    # Stop the timer and verify elapsed time, last value, and final log
    elapsed = t.stop()
    assert elapsed == 1.5
    assert t.last == 1.5
    assert logged == ["Starting timer test", "Elapsed: 1.5000s"]

    # Verify that the timer value was recorded in the shared Timers instance
    assert Timer.timers.total("test") == 1.5
    assert Timer.timers.count("test") == 1

    # Starting an already running timer should raise TimerError
    t.start()
    with pytest.raises(TimerError, match="Timer is running"):
        t.start()

    # Stopping an already stopped timer should raise TimerError
    t.stop()
    with pytest.raises(TimerError, match="Timer is not running"):
        t.stop()
