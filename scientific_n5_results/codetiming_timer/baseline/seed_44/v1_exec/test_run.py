import time
import pytest
from codetiming._timer import Timer

def test_timer_logging_and_elapsed_time(monkeypatch):
    logs = []

    def logger(msg):
        logs.append(msg)

    t = Timer(name="test", initial_text=True, logger=logger)

    # Patch perf_counter to return deterministic values
    counter = iter([100.0, 200.0])
    monkeypatch.setattr(time, "perf_counter", lambda: next(counter))

    t.start()
    assert logs == ["Timer test started"]

    elapsed = t.stop()
    assert elapsed == 100.0
    assert logs == ["Timer test started", "Elapsed time: 100.0000 seconds"]
