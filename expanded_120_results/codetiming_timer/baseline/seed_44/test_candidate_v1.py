import pytest
import codetiming._timer as _timer
import types

def test_timer_start_stop_and_logging(monkeypatch):
    # Capture logger output
    logs = []
    def logger(msg): logs.append(msg)

    # Mock perf_counter to produce deterministic elapsed time
    values = iter([1.0, 2.0])
    monkeypatch.setattr(_timer.time, "perf_counter", lambda: next(values))

    # Mock timers to record add calls
    mock_timers = types.SimpleNamespace(add=lambda name, elapsed: mock_timers.calls.append((name, elapsed)), calls=[])
    monkeypatch.setattr(_timer.Timer, "timers", mock_timers)

    # Test that starting an already running timer raises TimerError
    t = _timer.Timer(name="test", text="Elapsed: {:.2f}s", initial_text="Starting timer {name}", logger=logger)
    t.start()
    with pytest.raises(_timer.TimerError):
        t.start()

    # Test that stopping a timer that hasn't started raises TimerError
    t2 = _timer.Timer()
    with pytest.raises(_timer.TimerError):
        t2.stop()

    # Normal start/stop flow
    t3 = _timer.Timer(name="normal", text="Elapsed: {:.2f}s", initial_text="Starting timer {name}", logger=logger)
    t3.start()
    elapsed = t3.stop()
    assert elapsed == 1.0
    assert logs[0] == "Starting timer normal"
    assert logs[1] == "Elapsed: 1.00s"
    assert mock_timers.calls == [("normal", 1.0)]
