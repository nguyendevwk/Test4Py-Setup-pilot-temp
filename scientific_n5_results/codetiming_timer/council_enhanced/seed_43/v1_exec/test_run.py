import time
import pytest
from codetiming._timer import Timer, TimerError


def test_timer_stop_records_and_logs():
    logs = []

    def logger(msg: str) -> None:
        logs.append(msg)

    # Create a timer with a callable text formatter and custom logger
    t = Timer(name="perf", text=lambda elapsed: f"Elapsed: {elapsed:.4f}s", logger=logger)

    # Start the timer, sleep a short duration, then stop
    t.start()
    time.sleep(0.02)
    elapsed = t.stop()

    # Verify that elapsed time is a positive float
    assert isinstance(elapsed, float)
    assert elapsed > 0

    # Verify that the logger was called once with the formatted message
    assert len(logs) == 1
    assert logs[0] == f"Elapsed: {elapsed:.4f}s"

    # Verify that the timer's last attribute was updated
    assert t.last == elapsed

    # Verify that the timer's internal state is reset
    assert t._start_time is None

    # Verify that the global timers registry recorded the timing
    assert "perf" in t.timers.data
    assert pytest.approx(t.timers.data["perf"], rel=0.1) == elapsed
    assert pytest.approx(t.timers._timings["perf"][0], rel=0.1) == elapsed
