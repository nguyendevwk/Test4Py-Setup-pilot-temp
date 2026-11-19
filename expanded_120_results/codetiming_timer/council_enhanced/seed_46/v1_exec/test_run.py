import math
import pytest
from codetiming._timer import Timer, TimerError

def test_timer_context_manager_logging_and_timing(monkeypatch):
    # Simulate perf_counter returning 0 on start, 1.234 on stop
    counter_values = [0.0, 1.234]
    def mock_perf_counter():
        return counter_values.pop(0)
    monkeypatch.setattr("codetiming._timer.time.perf_counter", mock_perf_counter)

    logged = []
    def logger(msg: str) -> None:
        logged.append(msg)

    t = Timer(name="perf", text="Elapsed: {:0.4f}s", initial_text=True, logger=logger)

    # Use as context manager
    with t:
        pass  # nothing to do inside

    # After context, timer should have stopped
    assert math.isclose(t.last, 1.234, rel_tol=1e-9)
    # Logger should have received initial and final messages
    assert logged == ["Timer perf started", "Elapsed: 1.2340s"]
    # Timers collection should record the elapsed time
    assert t.timers.data["perf"] == 1.234
    assert t.timers._timings["perf"] == [1.234]
    # Starting again should raise TimerError because timer is not running
    with pytest.raises(TimerError, match="Timer is not running"):
        t.stop()
