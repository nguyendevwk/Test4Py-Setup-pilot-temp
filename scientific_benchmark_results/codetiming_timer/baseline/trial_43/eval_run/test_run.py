import pytest
from codetiming._timer import Timer, TimerError

def test_timer_start_stop_logging_and_elapsed(monkeypatch):
    logs = []
    recorded = []

    # Custom logger that records messages
    def logger(msg: str) -> None:
        logs.append(msg)

    # Mock perf_counter to return 100.0 on start, 100.5 on stop
    times = [100.0, 100.5]
    def mock_perf_counter():
        return times.pop(0)
    monkeypatch.setattr("codetiming._timer.time.perf_counter", mock_perf_counter)

    # Patch timers.add to capture calls
    def mock_add(name, elapsed):
        recorded.append((name, elapsed))
    monkeypatch.setattr(Timer.timers, "add", mock_add)

    # Create timer with custom text and initial_text
    t = Timer(
        name="test",
        text="Elapsed: {seconds:.2f}s",
        initial_text="Timer {name} started",
        logger=logger,
    )

    # Start the timer; should log initial text
    t.start()
    assert logs == ["Timer test started"]
    assert t._start_time is not None

    # Stop the timer; should log elapsed time and return elapsed
    elapsed = t.stop()
    assert elapsed == 0.5
    assert t.last == 0.5
    assert logs == ["Timer test started", "Elapsed: 0.50s"]
    assert recorded == [("test", 0.5)]

    # Subsequent stop should raise TimerError
    with pytest.raises(TimerError):
        t.stop()
