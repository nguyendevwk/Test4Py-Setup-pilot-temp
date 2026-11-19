import pytest
from codetiming._timer import Timer, TimerError

def test_timer_start_and_stop_logs_and_records(monkeypatch):
    logs = []

    def logger(msg: str) -> None:
        logs.append(msg)

    # Ensure timers dict is empty
    Timer.timers.clear()

    # Patch perf_counter to control elapsed time
    times = iter([100.0, 110.0])  # start at 100, stop at 110
    monkeypatch.setattr("codetiming._timer.time.perf_counter", lambda: next(times))

    t = Timer(name="test", initial_text="Starting timer {name}", text="Elapsed: {:0.4f}s", logger=logger)

    # Start timer: should log initial text
    t.start()
    assert logs == ["Starting timer test"]

    # Stop timer: should log elapsed time and record in timers
    elapsed = t.stop()
    assert elapsed == 10.0
    assert logs == ["Starting timer test", "Elapsed: 10.0000s"]
    assert Timer.timers.total("test") == 10.0
