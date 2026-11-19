import time
from codetiming._timer import Timer

def test_timer_context_manager_logging_and_timers(monkeypatch):
    logs = []

    def fake_logger(msg: str) -> None:
        logs.append(msg)

    # Simulate perf_counter: start at 100.0, after block 101.0
    counter_values = iter([100.0, 101.0])
    monkeypatch.setattr(time, "perf_counter", lambda: next(counter_values))

    t = Timer(name="test", text="Elapsed: {:0.4f}s", initial_text=True, logger=fake_logger)
    with t:
        pass

    # Verify elapsed time and state
    assert t.last == 1.0
    # Verify logger output
    assert logs[0] == "Timer test started"
    assert logs[1] == "Elapsed: 1.0000s"
    # Verify timers data
    assert t.timers.data["test"] == 1.0
    assert t.timers._timings["test"] == [1.0]
