import time
from codetiming._timer import Timer, TimerError

def test_timer_start_stop_logging_and_last_value(monkeypatch):
    logs = []

    def logger(msg):
        logs.append(msg)

    timer = Timer(
        name="test",
        initial_text="Timer {name} started",
        text="Elapsed: {seconds:.2f}s",
        logger=logger,
    )

    # Simulate perf_counter returning 100.0 at start and 101.5 at stop
    values = iter([100.0, 101.5])
    monkeypatch.setattr(time, "perf_counter", lambda: next(values))

    timer.start()
    assert logs == ["Timer test started"]

    timer.stop()
    assert logs == ["Timer test started", "Elapsed: 1.50s"]
    assert timer.last == 1.5
    assert timer._start_time is None
