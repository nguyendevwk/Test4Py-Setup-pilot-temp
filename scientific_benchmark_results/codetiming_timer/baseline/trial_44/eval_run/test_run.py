import codetiming._timer as _timer
import pytest

def test_timer_start_stop_logging_and_elapsed(monkeypatch):
    logs = []

    def logger(msg):
        logs.append(msg)

    t = _timer.Timer(
        name="test",
        initial_text="Starting timer {name}",
        text="Elapsed: {seconds:.2f}s",
        logger=logger,
    )

    # Simulate start time
    monkeypatch.setattr(_timer.time, "perf_counter", lambda: 100.0)
    t.start()
    assert logs == ["Starting timer test"]

    # Simulate stop time
    monkeypatch.setattr(_timer.time, "perf_counter", lambda: 110.0)
    elapsed = t.stop()
    assert elapsed == 10.0
    assert logs[-1] == "Elapsed: 10.00s"
    assert t._start_time is None
