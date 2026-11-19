import pytest
from codetiming import Timer, TimerError
import time

def test_stop_records_elapsed_and_updates_timers(monkeypatch):
    # Prepare a deterministic perf_counter sequence: start at 100, stop at 110
    counter = iter([100.0, 110.0])
    monkeypatch.setattr(time, "perf_counter", lambda: next(counter))

    # Capture logger output
    logs = []
    def logger(msg: str) -> None:
        logs.append(msg)

    # Ensure timers dict is clean
    Timer.timers.clear()

    t = Timer(name="perf", text="Elapsed: {:0.4f}s", logger=logger)
    t.start()
    elapsed = t.stop()

    # Verify elapsed time
    assert elapsed == 10.0
    assert t.last == 10.0

    # Verify logger output
    assert logs == ["Elapsed: 10.0000s"]

    # Verify timers data
    assert Timer.timers.data["perf"] == 10.0
    assert Timer.timers._timings["perf"] == [10.0]
